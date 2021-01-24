from useless import base
from useless.base import *


class Resolver(CMakePackage):
    def __init__(self):
        super().__init__()
        self.name = 'cereal'
        self.set('SKIP_PERFORMANCE_COMPARISON', 'ON')
        self.set('BUILD_TESTS', 'OFF')
        self.set('WITH_WERROR', 'OFF')

    def download(self):
        self.checkpoint('download', lambda: download_git(
            'https://github.com/USCiLab/cereal', self.src_dir))