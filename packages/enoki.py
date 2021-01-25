from useless import base
from useless.base import *


class Resolver(CMakePackage):
    def __init__(self):
        super().__init__()
        self.name = 'enoki'

    def build(self, config: str):
        if 'autodiff' in self.features:
            self.set('ENOKI_AUTODIFF', 'ON')
        if 'cuda' in self.features:
            self.set('ENOKI_CUDA', 'ON')
        if 'python' in self.features:
            self.set('ENOKI_PYTHON', 'ON')

        super().build(config)

    def download(self):
        self.checkpoint('download', lambda: download_git(
            'https://github.com/mitsuba-renderer/enoki/', self.src_dir))
        with open(self.src_dir+'CMakeLists.txt', 'r') as f:
            content = f.read()
        content += r'''
include(GNUInstallDirs)      
add_library(enoki INTERFACE)
target_include_directories(enoki INTERFACE $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>)

set(ENOKI_LIBRARIES enoki)
if (ENOKI_CUDA)
    set(ENOKI_LIBRARIES ${ENOKI_LIBRARIES} enoki-cuda)
endif()
if (ENOKI_AUTODIFF)
    set(ENOKI_LIBRARIES ${ENOKI_LIBRARIES} enoki-autodiff)
endif()
install(
    TARGETS ${ENOKI_LIBRARIES} EXPORT enoki-config
    RUNTIME DESTINATION ${CMAKE_INSTALL_BINDIR}/
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}/
    LIBRARY DESTINATION ${CMAKE_INSTALL_LIBDIR}/
)

install(
    EXPORT enoki-config DESTINATION ${CMAKE_INSTALL_DATAROOTDIR}/enoki
)

install(
    DIRECTORY ${CMAKE_SOURCE_DIR}/include/enoki
    DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
    FILES_MATCHING PATTERN "*.hpp*" PATTERN "*.inl*" PATTERN "*.h*"
)

'''
        with open(self.src_dir+'CMakeLists.txt', 'w') as f:
            f.write(content)
