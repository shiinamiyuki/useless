from useless import base
from useless.base import *


class Resolver(CMakePackage):
    def __init__(self):
        super().__init__()
        self.name = 'tinyobjloader'  
        self.set('CMAKE_POSITION_INDEPENDENT_CODE', 'TRUE')

    def download(self):
        self.checkpoint('download', lambda: download_git(
            'https://github.com/tinyobjloader/tinyobjloader', self.src_dir,tag='v2.0.0rc8'))
