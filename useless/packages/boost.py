from useless import base
from useless.base import *
import subprocess
import zipfile
import sys


class Solver(Package):
    def __init__(self):
        super().__init__()
        self.name = 'boost'

    def install(self, config: str):
        def install():
            subprocess.call([self.src_dir+'/b2.exe', "threading=multi", "address-model=64",
                             'release', 'install', '--prefix='+self.install_dir+'/boost'], cwd=self.src_dir)
        self.checkpoint('install', install)

    def build(self, config: str):
        # build_type = ''
        modules = []
        if 'system' in self.features:
            modules.append('system')
        if 'filesystem' in self.features:
            modules.append('filesystem')
        if 'regex' in self.features:
            modules.append('regex')
        if 'random' in self.features:
            modules.append('random')
        if 'stacktrace' in self.features:
            modules.append('stacktrace')
        if 'thread' in self.features:
            modules.append('thread')
        module_args = ['--with-'+x for x in modules]
        if sys.platform == 'linux':
            subprocess.call(['bash', './bootstrap.sh'], cwd=self.src_dir)
            subprocess.call(
                ['./b2', 'headers', "threading=multi", "address-model=64", 'release', '--prefix='+self.install_dir, *module_args], cwd=self.src_dir)
        else:
            def bootstrap():
                ret = subprocess.call(
                    ['cmd.exe', '/C', 'bootstrap.bat'], cwd=self.src_dir)
                assert ret == 0
            self.checkpoint('bootstrap', bootstrap)

            def build():
                subprocess.call(
                    [self.src_dir+'/b2.exe', "address-model=64", 'release'], cwd=self.src_dir)
                subprocess.call([self.src_dir+'/b2.exe', "threading=multi",
                                 "address-model=64", 'release', *module_args], cwd=self.src_dir)
            self.checkpoint('build', build)

    def download(self):
        self.checkpoint('download', lambda: download_git(
            'https://github.com/boostorg/boost', self.src_dir, recursive=True))
        # subprocess.call(['git', 'submodule', 'update',
        #                  '--init', '--recursive'], cwd=self.src_dir)
