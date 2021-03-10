from useless import base
from useless.base import *


class Resolver(CMakePackage):
    def __init__(self):
        super().__init__()
        self.name = 'gl3w'  
        self.set('CMAKE_POSITION_INDEPENDENT_CODE', 'TRUE')

    def download(self):
        self.checkpoint('download', lambda: download_git(
            'https://github.com/skaslev/gl3w', self.src_dir))
