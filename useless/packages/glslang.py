from useless import base
from useless.base import *


class Resolver(CMakePackage):
    def __init__(self):
        super().__init__()
        self.name = 'glslang'
        self.set('CMAKE_POSITION_INDEPENDENT_CODE', 'TRUE')

    def download(self):
        self.checkpoint('download', lambda: download_git(
            'https://github.com/KhronosGroup/glslang', self.src_dir, tag='vulkan-1.1-rc9'))
