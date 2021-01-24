from useless import base
from useless.base import *


class Resolver(CMakePackage):
    def __init__(self):
        super().__init__()
        self.name = 'tbb'
        self.set('TBB_TEST', 'OFF')
        self.set('TBB_EXAMPLES', 'OFF')
        self.set('TBB_STRICT', 'OFF')
        # self.set('CMAKE_POSITION_INDEPENDENT_CODE', 'TRUE')

    def download(self):
        self.checkpoint('download', lambda: download_git(
            'https://github.com/wjakob/tbb', self.src_dir))
