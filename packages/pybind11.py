from useless import base
from useless.base import *


class Resolver(CMakePackage):
    def __init__(self):
        super().__init__()
        self.name = 'pybind11'
        self.set('PYBIND11_TEST', 'OFF')

    def download(self):
        self.checkpoint('download', lambda: download_git(
            'https://github.com/pybind/pybind11', self.src_dir))