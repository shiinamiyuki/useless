from useless import base
from useless.base import *


class Resolver(CMakePackage):
    def __init__(self):
        super().__init__()
        self.name = 'fmt'
        self.set('FMT_TEST', 'OFF')
        self.set('CMAKE_POSITION_INDEPENDENT_CODE', 'TRUE')

    def download(self):
        self.checkpoint('download', lambda: download_git(
            'https://github.com/fmtlib/fmt', self.src_dir))
