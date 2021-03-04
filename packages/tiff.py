from useless import base
from useless.base import *
import subprocess
import zipfile
import sys
import os
import shutil

class Resolver(CMakePackage):
    def __init__(self):
        super().__init__()
        self.name = 'tiff'

    def download(self):
        version = '4.2.0'
        self.src_dir = self.base_src_dir + 'tiff-' + version + '/' 
        def F():
            download_file('https://download.osgeo.org/libtiff/tiff-{}.zip'.format(version),
                          dst=self.base_src_dir+'tiff.zip')
            with zipfile.ZipFile(self.base_src_dir+'tiff.zip') as zf:
                zf.extractall(self.base_src_dir)
            
        self.checkpoint('download', F)
