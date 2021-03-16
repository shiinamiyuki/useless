from useless import base
from useless.base import *


class Resolver(CMakePackage):
    def __init__(self):
        super().__init__()
        self.name = 'eigen3'
        self.set('EIGEN_TEST_CXX11', 'OFF')
        self.set('BUILD_TESTING', 'OFF')    

    def download(self):
        self.checkpoint('download', lambda: download_git(
            'https://gitlab.com/libeigen/eigen', self.src_dir,tag='3.4'))
