from useless import base
from useless.base import *


cmake_src = """
cmake_minimum_required(VERSION 3.12)
project(stb LANGUAGES C)
include(GNUInstallDirs)
add_library(stb_image stb_image.h stb_image.c)
add_library(stb::image ALIAS stb_image)
add_library(stb_image_write stb_image_write.h stb_image_write.c)
add_library(stb::image_write ALIAS stb_image)

install(TARGETS stb_image stb_image_write
    EXPORT stb-config
    DESTINATION lib)

install(
    EXPORT stb-config DESTINATION ${CMAKE_INSTALL_DATAROOTDIR}/stb
)

install(
    DIRECTORY ${CMAKE_SOURCE_DIR}
    DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}/
    FILES_MATCHING PATTERN "*.hpp*" PATTERN "*.inl*" PATTERN "*.h*"
)


"""

stb_image_c = """
#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"
"""
stb_image_write_c = """
#define STB_IMAGE_WRITE_IMPLEMENTATION
#include "stb_image_write.h"
"""


class Solver(CMakePackage):
    def __init__(self):
        super().__init__()
        self.name = 'stb'

    def download(self):
        def F():
            download_git(
                'https://github.com/nothings/stb', self.src_dir)
            with open(self.src_dir+'CMakeLists.txt', 'w') as f:
                f.write(cmake_src)
            with open(self.src_dir+'stb_image.c', 'w') as f:
                f.write(stb_image_c)
            with open(self.src_dir+'stb_image_write.c', 'w') as f:
                f.write(stb_image_write_c)
        self.checkpoint('download', F)
