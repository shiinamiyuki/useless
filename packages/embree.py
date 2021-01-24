from useless import base
from useless.base import *


class Resolver(CMakePackage):
    def __init__(self):
        super().__init__()
        self.name = 'embree'
        self.set('EMBREE_TASKING_SYSTEM', 'INTERNAL')
        self.set('EMBREE_ISPC_SUPPORT', 'OFF')
        self.set('EMBREE_TUTORIALS', 'OFF')

    def download(self):
        self.checkpoint('download', lambda: download_git(
            'https://github.com/embree/embree', self.src_dir))
