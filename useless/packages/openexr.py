from useless import base
from useless.base import *


class Solver(CMakePackage):
    def __init__(self):
        super().__init__()
        self.name = 'openexr'
        self.set('OPENEXR_BUILD_SHARED_LIBS', "OFF")
        self.set('OPENEXR_BUILD_SHARED_LIBS', "OFF")
        self.set('ILMBASE_BUILD_SHARED_LIBS', "OFF")
        self.depends(resolve_package('zlib'))

    def download(self):
        self.checkpoint('download', lambda: download_git(
            'https://github.com/AcademySoftwareFoundation/openexr', self.src_dir))
