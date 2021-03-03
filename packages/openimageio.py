from useless import base
from useless.base import *


class Resolver(CMakePackage):
    def __init__(self):
        super().__init__()
        self.name = 'openimageio'
        self.set('OPENEXR_BUILD_SHARED_LIBS', "OFF")
        self.set('OPENEXR_BUILD_SHARED_LIBS', "OFF")
        self.set('ILMBASE_BUILD_SHARED_LIBS', "OFF")
        self.set('USE_PYTHON','OFF')
        self.depends(require('openexr'))
        boost = require('boost')
        self.depends(boost)
        boost.enable('system')
        boost.enable('random')
        boost.enable('regex')
        boost.enable('thread')
        boost.enable('filesystem')
        boost.enable('stacktrace')

    def setup(self, src_dir, build_dir, install_dir):
        super().setup(src_dir, build_dir, install_dir)
        self.set('Boost_ROOT', src_dir+'/boost/')

    def download(self):
        self.checkpoint('download', lambda: download_git(
            'https://github.com/OpenImageIO/oiio', self.src_dir))
