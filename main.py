import os
import sys
import json
import subprocess
import pathlib
import shutil
import multiprocessing
import importlib
import useless
import useless.base
# from functools import cache

dir_path = os.path.dirname(os.path.realpath(__file__))
assert dir_path == os.getcwd()
dir_path = dir_path.replace('\\', '/')
WORKSPACE_DIR = dir_path + '/.useless/'
PKG_DIR = dir_path + '/useless/packages/'
SRC_DIR = dir_path + '/.useless/source/'
BUILD_DIR = dir_path + '/.useless/build/'
INSTALL_DIR = dir_path + '/.useless/install/'


def find_dependencies(package):
    with open(PKG_DIR + package + '.json') as f:
        config = json.load(f)
        assert config['name'] == package
        dependencies = config.get('depends', [])
    res = set(dependencies)
    for dep in dependencies:
        res = res.union(find_dependencies(dep))
    return res


def remove(package):
    shutil.rmtree(SRC_DIR + package)
    shutil.rmtree(BUILD_DIR + package)
    shutil.rmtree(INSTALL_DIR + package)


def install(package_name):
    # src_dir = SRC_DIR
    # build_dir = BUILD_DIR
    # install_dir = INSTALL_DIR

    config = 'Release'
    # spec = importlib.util.spec_from_file_location(
    #     package_name, PKG_DIR + package_name + '.py')
    # m = importlib.util.module_from_spec(spec)
    # spec.loader.exec_module(m)
    # package = m.Solver()  # shit name
    # package.setup(src_dir, build_dir, install_dir)
    # package.download()
    # package.build(config)
    # package.install(config)
    useless.base.setup(PKG_DIR, SRC_DIR, BUILD_DIR, INSTALL_DIR)
    package = useless.base.resolve_package(package_name)
    useless.base.add_dependency(package, None)
    useless.base.run_build_graph(config)


def check_init():
    if not os.path.isdir(WORKSPACE_DIR):
        os.mkdir(WORKSPACE_DIR)
    if not os.path.isdir(PKG_DIR):
        os.mkdir(PKG_DIR)
    if not os.path.isdir(SRC_DIR):
        os.mkdir(SRC_DIR)
    if not os.path.isdir(BUILD_DIR):
        os.mkdir(BUILD_DIR)
    if not os.path.isdir(INSTALL_DIR):
        os.mkdir(INSTALL_DIR)


def yn():
    while True:
        x = input()
        if x == 'Y' or x == 'y':
            return True
        if x == 'N' or x == 'n':
            return False


def extract_opts(argv):
    opts = []
    args = []
    for i in argv:
        if i.startswith('--'):
            opts.append(i)
        else:
            args.append(i)
    return opts, args


def main(argv):
    if len(argv) < 2:
        exit(1)
    check_init()
    cmd = argv[1]
    if cmd == 'install':
        opts, packages = extract_opts(argv[2:])
        for package in packages:
            install(package)
    # if cmd == 'install':
    #     all_packages = []
    #     opts, packages = extract_opts(argv[2:])
    #     for package in packages:
    #         if check_is_installed(package):
    #             print('package {} already installed'.format(package))
    #             continue
    #         all_packages.append(package)
    #         deps = find_dependencies(package)
    #         all_packages.extend(list(deps))
    #     print('The following packages will be installed:')
    #     for pkg in all_packages:
    #         if not check_is_installed(pkg):
    #             print('  ', pkg)
    #     if '--quiet' not in opts:
    #         print('Continue [Y/N]')
    #         if yn():
    #             for package in packages:
    #                 install(package)
    #     else:
    #         for package in packages:
    #             install(package)
    # if cmd == 'remove':
    #     for package in argv[2:]:
    #         if not check_is_installed(package):
    #             print('package {} is not installed'.format(package))
    #             exit(1)
    #         remove(package)


if __name__ == "__main__":
    main(sys.argv)
