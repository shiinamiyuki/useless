import os
import sys
import json
import subprocess
import pathlib
import shutil
import multiprocessing
import abc
import importlib
import requests

PKG_DIR = ''
SRC_DIR = ''
BUILD_DIR = ''
INSTALL_DIR = ''
GENERATOR = ''


def touch(path):
    with open(path, 'a'):
        os.utime(path, None)


def touch_if_none(path):
    if not os.path.isfile(path):
        touch(path)


def mkdir_if_none(path):
    if not os.path.isdir(path):
        os.mkdir(path)


def mtime(path):
    fname = pathlib.Path(path)
    assert fname.exists(), f'No such file: {fname}'
    return fname.stat().st_mtime_ns


def is_older(path1, path2):
    return mtime(path1) < mtime(path2)


def download_git(url, src_dir, recursive=True, shallow=True, tag=None):
    args = ['git', 'clone']
    if recursive:
        args.append('--recursive')
    if shallow:
        args.extend(['--depth', '1'])
    if tag:
        args.extend(['--branch', tag])
    args.extend([url, src_dir])
    args.extend(['--jobs', str(multiprocessing.cpu_count())])
    ret = subprocess.call(args)
    if ret:
        print('git clone failed with code ',
              ret, file=sys.stderr)
        exit(1)


def download_file(url: str, dst):
    r = requests.get(url, allow_redirects=True)
    with open(dst, 'wb') as f:
        f.write(r.content)


dependency_graph = dict()
# A deps B


def add_dependency(A, B):
    # print(A, B, dependency_graph)
    if A not in dependency_graph:
        dependency_graph[A] = []
    if B is None:
        # print(dependency_graph)
        return
    if B not in dependency_graph:
        dependency_graph[B] = []
    if A in dependency_graph[B]:
        print('cyclic dependency between package {} and {}'.format(
            A.name, B.name), file=sys.stderr)
        exit(1)
    if B not in dependency_graph[A]:
        dependency_graph[A].append(B)
    # print(dependency_graph)


class Package:
    src_dir: str
    build_dir: str
    install_dir: str
    _checkpoints: list
    name: str
    features: set
    base_src_dir: str
    base_build_dir: str

    def __init__(self):
        self.features = set()

    def setup(self, src_dir, build_dir, install_dir):
        self.base_build_dir = build_dir
        self.base_src_dir = src_dir
        self.src_dir = src_dir + self.name + '/'
        self.build_dir = build_dir + self.name + '/'
        self.install_dir = install_dir
        mkdir_if_none(self.src_dir)
        mkdir_if_none(self.build_dir)
        mkdir_if_none(self.install_dir)
        self._checkpoints = []

        def dummy():
            pass
        self.checkpoint('__init__', dummy)

    def enable(self, feature):
        self.features.add(feature)

    @abc.abstractmethod
    def build(self, config: str):
        pass

    @abc.abstractmethod
    def download(self):
        pass

    @abc.abstractmethod
    def install(self, config: str):
        pass

    def checkpoint(self, label: str, action: callable):
        f = self.build_dir + '.checkpoint.' + label
        if not os.path.isfile(f) or (self._checkpoints and is_older(f, self._checkpoints[-1])):
            action()
            touch_if_none(f)
        self._checkpoints.append(f)

    def depends(self, package: "Package"):
        add_dependency(self, package)


class CMakePackage(Package):
    options: dict
    
    def __init__(self):
        super().__init__()
        self.options = dict()

    def setup(self, src_dir, build_dir, install_dir):
        super().setup(src_dir, build_dir, install_dir)

        self.set('CMAKE_INSTALL_PREFIX', install_dir)
        self.set('CMAKE_PREFIX_PATH', install_dir)

    def set(self, opt, val):
        self.options[opt] = val

    def build(self, config: str):
        config_args = ['-D{}={}'.format(k, self.options[k])
                       for k in self.options]
        generator_args = []
        if GENERATOR is not None:
            generator_args = ['-G'+GENERATOR]

        def run_config():
            ret = subprocess.call(
                ['cmake', self.src_dir, *generator_args, '-DCMAKE_BUILD_TYPE='+config, *config_args], cwd=self.build_dir)
            if ret != 0:
                print('cmake configure failed with code ',
                      ret, file=sys.stderr)
                exit(1)
        self.checkpoint('config', run_config)

        def run_build():
            target_all = 'all'
            if sys.platform == 'win32':
                target_all = 'ALL_BUILD'
            geneator_args = []
            if sys.platform == 'linux':
                geneator_args = ['-j', str(multiprocessing.cpu_count())]
            ret = subprocess.call(
                ['cmake', '--build', '.', '--config', config, '--target', target_all, '--', *geneator_args], cwd=self.build_dir)
            if ret != 0:
                print('build failed with code ', ret, file=sys.stderr)
                exit(1)
        self.checkpoint('build', run_build)

    def install(self, config: str):
        def run_install():
            target_install = 'install'
            if sys.platform == 'win32':
                target_install = 'INSTALL'
            ret = subprocess.call(
                ['cmake', '--build', self.build_dir, '--config', config, '--target', target_install], cwd=self.build_dir)
            if ret != 0:
                print('install failed with code ', ret, file=sys.stderr)
                exit(1)
        self.checkpoint('install', run_install)


def __require():
    cache = dict()

    def F(package_name):
        if package_name in cache:
            return cache[package_name]
        # spec = importlib.util.spec_from_file_location(
        #     package_name, PKG_DIR + package_name + '.py')
        # m = importlib.util.module_from_spec(spec)
        importlib.import_module('useless.packages')
        m = importlib.import_module('useless.packages.' + package_name)
        # spec.loader.exec_module(m)
        package = m.Resolver()
        cache[package_name] = package
        add_dependency(package, None)
        return package

    return F


require = __require()


def is_cmd_available(cmd):
    return shutil.which(cmd) is not None


def __init_generator():
    global GENERATOR
    if GENERATOR is None:
        if sys.platform == 'linux' or sys.platform == 'darwin':
            if is_cmd_available('ninja'):
                GENERATOR = 'Ninja'
            else:
                GENERATOR = None
        # elif sys.platform == 'win32':
        #     GENERATOR = 'Ninja'
        #     if not is_cmd_available('ninja'):
        #         download_file(
        #             'https://github.com/ninja-build/ninja/releases/download/v1.10.2/ninja-win.zip', BUILD_DIR + 'ninja.zip')
        #         import zipfile
        #         with zipfile.ZipFile(BUILD_DIR + 'ninja.zip') as zf:
        #             zf.extractall(BUILD_DIR)
        #         # print(os.environ)
        #         os.environ['PATH'] += BUILD_DIR


def setup(pkg_dir, src_dir, build_dir, install_dir, generator=None):
    global SRC_DIR
    global BUILD_DIR
    global INSTALL_DIR
    global PKG_DIR
    global GENERATOR
    GENERATOR = generator
    PKG_DIR = pkg_dir
    SRC_DIR = src_dir
    BUILD_DIR = build_dir
    INSTALL_DIR = install_dir
    __init_generator()


def topo_sort(graph: dict):
    vertices = set()
    for k in graph:
        vertices.add(k)
        vertices = vertices.union(graph[k])
    permanent = set()
    temp = set()
    L = list()

    def visit(v):
        if v in permanent:
            return
        if v in temp:
            raise RuntimeError("cyclic dependency!")
        temp.add(v)

        for u in graph[v]:
            visit(u)
        temp.remove(v)
        permanent.add(v)
        L.append(v)

    while len(vertices) > 0:
        v = vertices.pop()
        if v not in permanent:
            visit(v)
    return L


def run_build_graph(config):
    order = topo_sort(dependency_graph)
    # print(dependency_graph)
    # print(order)
    for package in order:
        package.setup(SRC_DIR, BUILD_DIR, INSTALL_DIR)
        package.download()
        package.build(config)
        package.install(config)
