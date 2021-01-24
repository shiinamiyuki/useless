from useless import base
from useless.base import *


class Resolver(CMakePackage):
    def __init__(self):
        super().__init__()
        self.name = 'assimp'
        self.set('ASSIMP_BUILD_TESTS', "OFF")
        self.set('BUILD_SHARED_LIBS', "OFF")
        self.depends(resolve_package('zlib'))

    def download(self):
        self.checkpoint('download', lambda: download_git(
            'https://github.com/assimp/assimp', self.src_dir))
