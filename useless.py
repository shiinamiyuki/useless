import os
import sys
import json
import subprocess
import pathlib

dir_path = os.path.dirname(os.path.realpath(__file__))
assert dir_path == os.getcwd()
dir_path = dir_path.replace('\\','/')
WORKSPACE_DIR = dir_path + '/.useless/'
PKG_DIR = dir_path + '/packages/'
SRC_DIR = dir_path + '/.useless/source/'
BUILD_DIR = dir_path + '/.useless/build/'
INSTALL_DIR = dir_path + '/.useless/install/'


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
    return fname.stat().st_mtime


def is_older(path1, path2):
    return mtime(path1) < mtime(path2)

def check_is_installed(package):
    src_stamp = SRC_DIR + package + '/.source'
    build_stamp = SRC_DIR + package + '/.build'
    install_stamp = SRC_DIR + package + '/.install'
    if not os.path.exists(src_stamp) or not os.path.exists(build_stamp) or not os.path.exists(install_stamp):
        return False
    return is_older(src_stamp, build_stamp) and is_older(build_stamp, install_stamp)

def install(package):
    if check_is_installed(package):
        print('package {} already installed'.format(package))
    with open(PKG_DIR + package + '.json') as f:
        config = json.load(f)
        assert config['name'] == package
        dependencies = config.get('depends', [])
        for dep in dependencies:
            install(dep)
        src_stamp = SRC_DIR + package + '/.source'
        build_stamp = SRC_DIR + package + '/.build'
        install_stamp = SRC_DIR + package + '/.install'
        src_dir = SRC_DIR + package
        build_dir = BUILD_DIR + package
        # install_dir = INSTALL_DIR + package
        if not os.path.isdir(SRC_DIR + package):
            repo = config['repository']
            subprocess.call(['git', 'clone', '--depth', '1',
                             repo['git'], src_dir], cwd=dir_path)
            touch_if_none(src_stamp)

        if not os.path.exists(build_stamp) or is_older(build_stamp, src_stamp):
            mkdir_if_none(build_dir)
            config_args = config.get('cmake-configure', [])
            ret = subprocess.call(['cmake', src_dir, '-DCMAKE_BUILD_TYPE=Release',
                                   '-DCMAKE_INSTALL_PREFIX={}'.format(
                                       INSTALL_DIR),
                                   '-DCMAKE_MODULE_PATH={}'.format(INSTALL_DIR), *config_args], cwd=build_dir)
            if ret != 0:
                print('cmake configure failed with code ', ret, file=sys.stderr)
                exit(1)
            target_all = 'all'
            if sys.platform == 'win32':
                target_all = 'ALL_BUILD'

            ret = subprocess.call(
                ['cmake', '--build', '.', '--config', 'Release', '--target', target_all], cwd=build_dir)
            if ret != 0:
                print('build failed with code ', ret, file=sys.stderr)
                exit(1)
            touch_if_none(build_stamp)
        if not os.path.exists(install_stamp) or is_older(install_stamp, build_stamp):
            target_install = 'install'
            if sys.platform == 'win32':
                target_install = 'INSTALL'
            ret = subprocess.call(
                ['cmake', '--build', build_dir, '--config', 'Release', '--target', target_install], cwd=build_dir)
            if ret != 0:
                print('install failed with code ', ret, file=sys.stderr)
                exit(1)
            touch_if_none(install_stamp)
        print('package {} installed'.format(package))


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


def main(argv):
    if len(argv) < 2:
        exit(1)
    check_init()
    cmd = argv[1]
    if cmd == 'install':
        for package in argv[2:]:
            install(package)


if __name__ == "__main__":
    main(sys.argv)
