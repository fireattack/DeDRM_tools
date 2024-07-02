from DeDRM_plugin.kindlekey import getkey
from DeDRM_plugin.k4mobidedrm import decryptBook

from pathlib import Path

raw_file = Path('tests/B0D7VF6BRQ_EBOK.azw')
for f in Path('tests').iterdir():
    if not f == raw_file:
        f.unlink()

getkey('tests')
decryptBook('tests/B0D7VF6BRQ_EBOK.azw', 'tests', ['tests/kindlekey1.k4i'], [], [], [])

