from DeDRM_plugin.kindlekey import getkey
from DeDRM_plugin.k4mobidedrm import decryptBook

from pathlib import Path

raw_file = [Path('tests/B0D7VF6BRQ_EBOK.azw'), Path('tests/B07PMHZX48_EBOK.azw')]
for f in Path('tests').iterdir():
    if not f in raw_file:
        f.unlink()

getkey('tests')
try:
    decryptBook('tests/B0D7VF6BRQ_EBOK.azw', 'tests', ['tests/kindlekey1.k4i'], [], [], [])
except:
    print('Decrypt B0D7VF6BRQ_EBOK failed')
try:
    decryptBook('tests/B07PMHZX48_EBOK.azw', 'tests', ['tests/kindlekey1.k4i'], [], [], [])
except:
    print('Decrypt B07PMHZX48_EBOK failed')

