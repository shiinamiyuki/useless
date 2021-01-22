from useless import base
from useless.base import *


class Solver(CMakePackage):
    def __init__(self):
        super().__init__()
        self.name = 'spdlog'
        self.depends(resolve_package('fmt'))

    def download(self):
        self.checkpoint('download', lambda: download_git(
            'https://github.com/gabime/spdlog', self.src_dir))
