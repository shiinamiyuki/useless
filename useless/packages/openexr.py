from useless import base
from useless.base import *


class Resolver(CMakePackage):
    def __init__(self):
        super().__init__()
        self.name = 'openexr'
        self.depends(require('zlib'))
        self.set('PYILMBASE_ENABLE', 'OFF')

    def download(self):
        self.checkpoint('download', lambda: download_git(
            'https://github.com/AcademySoftwareFoundation/openexr', self.src_dir,tag='v2.5.4'))
