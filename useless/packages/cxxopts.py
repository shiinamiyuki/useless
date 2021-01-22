from useless import base
from useless.base import *


class Solver(CMakePackage):
    def __init__(self):
        super().__init__()
        self.name = 'cxxopts'
        self.set('CXXOPTS_BUILT_TESTS', 'OFF')
        self.set('CXXOPTS_BUILT_EXAMPLES', 'OFF')

    def download(self):
        self.checkpoint('download', lambda: download_git(
            'https://github.com/jarro2783/cxxopts', self.src_dir))
