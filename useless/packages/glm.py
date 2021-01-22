from useless import base
from useless.base import *


class Solver(CMakePackage):
    def __init__(self):
        super().__init__()
        self.name = 'glm'
        self.set('GLM_TEST_ENABLE', 'OFF')

    def download(self):
        self.checkpoint('download', lambda: download_git(
            'https://github.com/g-truc/glm', self.src_dir))
        with open(self.src_dir+'CMakeLists.txt', 'r') as f:
            cmake = f.read()
        cmake += """

install(DIRECTORY glm DESTINATION include )

"""
        with open(self.src_dir+'CMakeLists.txt', 'w') as f:
            f.write(cmake)