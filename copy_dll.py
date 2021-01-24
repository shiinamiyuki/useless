import sys
import shutil
import os
import glob

if __name__ == '__main__':
    assert len(sys.argv) == 3
    src_dir = sys.argv[1]
    dst_dir = sys.argv[2]
    src_dir = src_dir.replace('\\','/')
    if not src_dir.endswith('/'):
        src_dir += '/'
    dst_dir = dst_dir.replace('\\','/')
    if not dst_dir.endswith('/'):
        dst_dir += '/'
    for filename in os.listdir(src_dir):
        _, ext = os.path.splitext(filename)
        if ext in ['.dll', '.so']:
            print('copying ' + filename + ' -> ' + dst_dir + filename)
            shutil.copyfile(src_dir + filename, dst_dir + filename)