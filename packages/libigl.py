from useless import base
from useless.base import *


class Resolver(CMakePackage):
    def __init__(self):
        super().__init__()
        self.name = 'libigl'
        

    def download(self):
        self.checkpoint('download', lambda: download_git(
            'https://github.com/libigl/libigl/', self.src_dir,tag='v2.2.0'))
        with open(self.src_dir+'cmake/libigl.cmake', 'r') as f:
            content = f.read()
        content = content.replace('if(HUNTER_ENABLED)', 'if(TRUE)')
        content = content.replace('hunter_add_package(Eigen)', '')
