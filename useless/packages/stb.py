from useless import base
from useless.base import *


cmake_src = """
cmake_minimum_required(VERSION 3.12)
project(stb)

add_library(stb_image stb_image.h stb_image.c)
add_library(stb::image ALIAS stb_image)

file(GLOB headers stb_*.h)


install(TARGETS stb_image DESTINATION lib)
install(FILES ${headers} DESTINATION include )


"""

stb_image_c = """
#define STB_IMAGE_IMPLEMENTATION
#include "stb_image.h"
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
        self.checkpoint('download', F)
