"""
* unzip images into root directory
"""

from pathlib import Path
from zipfile import ZipFile
from pprint import pprint
import sys

root_d = Path(__file__).resolve().parent

zip_fn = root_d / 'Anomaly_PyCV_test_task.zip'
assert zip_fn.is_file()
with ZipFile(str(zip_fn), 'r') as zip:
    zip.extractall()

imgry_d = root_d / 'Anomaly_PyCV_test_task' / 'Test_aerial_imagery'
assert imgry_d.is_dir()
for fn in imgry_d.glob('*.zip'):
    arch_d = imgry_d / fn.resolve().stem    # directory for this archive
    arch_d.mkdir(parents=True, exist_ok=True)
    with ZipFile(str(fn), 'r') as zip:
        zip.extractall(str(arch_d))