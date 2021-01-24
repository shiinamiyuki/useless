from useless import base
from useless.base import *


class Resolver(CMakePackage):
    def __init__(self):
        super().__init__()
        self.name = 'glfw'
        self.set('GLFW_BUILD_TESTS', 'OFF')
        self.set('GLFW_BUILD_EXAMPLES', 'OFF')    
        self.set('GLFW_BUILD_DOCS', 'OFF')    
        self.set('CMAKE_POSITION_INDEPENDENT_CODE', 'TRUE')

    def download(self):
        self.checkpoint('download', lambda: download_git(
            'https://github.com/glfw/glfw/', self.src_dir,tag='3.3.2'))
