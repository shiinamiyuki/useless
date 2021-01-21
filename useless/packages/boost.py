from useless import base
from useless.base import *
import subprocess
import zipfile


class Solver(Package):
    def __init__(self):
        super().__init__()
        self.name = 'boost'

    def install(self, config: str):
        pass

    def build(self, config: str):
        subprocess.call(['bash', './bootstrap.sh'], cwd=self.src_dir)
        subprocess.call(['./b2', 'headers'], cwd=self.src_dir)

    def download(self):
        self.checkpoint('download', lambda: download_git(
            'https://github.com/boostorg/boost', self.src_dir, recursive=True))
        # subprocess.call(['git', 'submodule', 'update',
        #                  '--init', '--recursive'], cwd=self.src_dir)
        

