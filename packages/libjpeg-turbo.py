

from useless import base
from useless.base import *
from shutil import copyfile
import os


class Resolver(CMakePackage):
    def __init__(self):
        super().__init__()
        self.name = 'libjpeg-turbo'

    def download(self):
        self.checkpoint('download', lambda: download_git(
            'https://github.com/libjpeg-turbo/libjpeg-turbo', self.src_dir,tag='2.0.90'))