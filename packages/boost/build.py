import sys
import subprocess

if __name__ == "__main__":
    src_dir = sys.argv[1]
    build_dir = sys.argv[2]
    install_dir = sys.argv[3]
    subprocess.call(['bash', './bootstrap.sh'], cwd=src_dir)
    subprocess.call(['./b2', 'headers'], cwd=src_dir)