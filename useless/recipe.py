from useless import base
import os

class Recipe:
    config: str

    def __init__(self, config: str, useless_dir: str):
        self.config = config
        useless_dir = os.path.abspath(useless_dir)
        WORKSPACE_DIR = useless_dir + '/.useless/'
        PKG_DIR = useless_dir + '/useless/packages/'
        SRC_DIR = useless_dir + '/.useless/source/'
        BUILD_DIR = useless_dir + '/.useless/build/'
        INSTALL_DIR = useless_dir + '/.useless/install/'
        if not os.path.isdir(WORKSPACE_DIR):
            os.mkdir(WORKSPACE_DIR)
        if not os.path.isdir(PKG_DIR):
            os.mkdir(PKG_DIR)
        if not os.path.isdir(SRC_DIR):
            os.mkdir(SRC_DIR)
        if not os.path.isdir(BUILD_DIR):
            os.mkdir(BUILD_DIR)
        if not os.path.isdir(INSTALL_DIR):
            os.mkdir(INSTALL_DIR)
        base.setup(PKG_DIR, SRC_DIR, BUILD_DIR, INSTALL_DIR)

    def require(self, package: str):
        return base.require(package)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        base.run_build_graph(self.config)

# def begin(config, useless_dir):
#     return Recipe(config, useless_dir)