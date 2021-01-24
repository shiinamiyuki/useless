from useless import base
from useless.base import *


class Resolver(CMakePackage):
    def __init__(self):
        super().__init__()
        self.name = 'openvdb'
        self.depends(require('openexr'))
        self.depends(require('tbb'))
        self.depends(require('boost'))
        self.set('USE_BLOSC','OFF')
        self.set('USE_EXR', 'ON')

    def setup(self, src_dir, build_dir, install_dir):
        super().setup(src_dir, build_dir, install_dir)
        self.set('Boost_ROOT', src_dir+'/boost/')
        # self.set('CMAKE_POSITION_INDEPENDENT_CODE', 'TRUE')

    def download(self):
        self.checkpoint('download', lambda: download_git(
            'https://github.com/AcademySoftwareFoundation/openvdb', self.src_dir, tag='v8.0.0'))
