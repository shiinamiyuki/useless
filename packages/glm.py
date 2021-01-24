from useless import base
from useless.base import *


class Resolver(CMakePackage):
    def __init__(self):
        super().__init__()
        self.name = 'glm'
        self.set('GLM_TEST_ENABLE', 'OFF')

    def download(self):
        self.checkpoint('download', lambda: download_git(
            'https://github.com/g-truc/glm', self.src_dir))
#         with open(self.src_dir+'CMakeLists.txt', 'r') as f:
#             cmake = f.read()
#         cmake += """

# install(DIRECTORY glm DESTINATION include )
# install(TARGETS glm
#     EXPORT glmConfig)
# export(TARGETS
#         glm
#     NAMESPACE glm::
#     FILE "${CMAKE_CURRENT_BINARY_DIR}/glmConfig.cmake"
# )
# install(EXPORT
#         glmConfig
#     DESTINATION "${CMAKE_INSTALL_DATADIR}/glm/cmake"
#     NAMESPACE glm::
# )
# """
        with open(self.src_dir+'CMakeLists.txt', 'w') as f:
            f.write("""cmake_minimum_required(VERSION 3.12 FATAL_ERROR)

project(glm LANGUAGES CXX)

include(GNUInstallDirs)

add_library(glm INTERFACE)
target_include_directories(glm INTERFACE $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>)

install(
    TARGETS glm EXPORT glm-config
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}/
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}/
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}/
)

install(
    EXPORT glm-config DESTINATION ${CMAKE_INSTALL_DATAROOTDIR}/glm
)

install(
    DIRECTORY ${CMAKE_SOURCE_DIR}/glm
    DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
    FILES_MATCHING PATTERN "*.hpp*" PATTERN "*.inl*" PATTERN "*.h*"
)
""")