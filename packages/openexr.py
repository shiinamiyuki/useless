from useless.base import *
import sys

class Resolver(CMakePackage):
    def __init__(self):
        super().__init__()
        self.name = 'openexr'
        self.depends(require('zlib'))
        self.set('PYILMBASE_ENABLE', 'OFF')
        if sys.platform == 'win32' and GENERATOR is None:
            self.set('CMAKE_CXX_FLAGS', '/MP')

    def download(self):
        self.checkpoint('download', lambda: download_git(
            'https://github.com/AcademySoftwareFoundation/openexr', self.src_dir,tag='v2.5.4'))
