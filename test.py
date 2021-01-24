import sys
sys.path.append('./useless')
import useless
import useless.base
from useless.recipe import Recipe

if __name__ == '__main__':
    with Recipe('Release', '.') as r:
        assert r
        r.require('openexr')
        r.require('zlib')
