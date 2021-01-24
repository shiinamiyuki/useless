from useless import base
from useless.base import *


class Resolver(CMakePackage):
    def __init__(self):
        super().__init__()
        self.name = 'spdlog'
        self.depends(resolve_package('fmt'))
        self.set('CMAKE_POSITION_INDEPENDENT_CODE', 'TRUE')

    def download(self):
        self.checkpoint('download', lambda: download_git(
            'https://github.com/gabime/spdlog', self.src_dir))
