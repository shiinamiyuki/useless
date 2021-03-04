

from useless import base
from useless.base import *


class Resolver(CMakePackage):
    def __init__(self):
        super().__init__()
        self.name = 'libpng'

    def download(self):
        self.checkpoint('download', lambda: download_git(
            'https://github.com/mitsuba-renderer/libpng', self.src_dir))
