

from useless import base
from useless.base import *
from shutil import copyfile
import os


class Resolver(CMakePackage):
    def __init__(self):
        super().__init__()
        self.name = 'libjpeg'

    def install(self, config: str):
        super().install(config)
        for filename in os.listdir(self.install_dir + '/include/libjpeg/'):
            if filename.endswith('.h'):
                copyfile(self.install_dir + 'include/libjpeg/' +
                         filename, self.install_dir + 'include/' + filename)
        with open(self.install_dir + 'include/libjpeg/jconfig.h.cmake') as f:
            content = f.read()
        # assert '#cmakedefine' in content
        content = content.replace('#cmakedefine', '#define')
        # print(content)
        # assert '#cmakedefine' not in content
        with open(self.install_dir + 'include/jconfig.h', 'w') as f:
            f.write(content)

    def download(self):
        self.checkpoint('download', lambda: download_git(
            'https://github.com/mitsuba-renderer/libjpeg', self.src_dir))
        with open(self.src_dir+'CMakeLists.txt', 'r') as f:
            content = f.read()
        content += r'''
include(GNUInstallDirs)    
install(
    TARGETS jpeg djpeg cjpeg EXPORT libjpeg-config
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}/
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}/
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}/
)

install(
    EXPORT libjpeg-config DESTINATION ${CMAKE_INSTALL_DATAROOTDIR}/
)

install(
    DIRECTORY ${CMAKE_SOURCE_DIR}
    DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
    FILES_MATCHING PATTERN "*.hpp*" PATTERN "*.inl*" PATTERN "*.h*"
)
        '''
        with open(self.src_dir+'CMakeLists.txt', 'w') as f:
            f.write(content)
