from __future__ import print_function

try:
    from pathlib import Path
except ImportError:
    pass

import cv2
import sys
from gdalcopyproj import cp_proj        # this used to copy geotiff meta data into processed files

def do_he(fn):
    grey = cv2.imread(fn, 0)
    grey_eq = cv2.equalizeHist(grey)

    # remove black background while here too
    # TODO: Todd said 255 is mask value. use this
    height, width = grey_eq.shape
    corners = [(0,0), (width-1,height-1), (width-1,0), (0,height-1)]
    for corner in corners:
        cv2.floodFill(grey_eq, mask=None, seedPoint=corner, newVal=255);

    return grey_eq

def main():
    for d in [fn for fn in Path(r"Anomaly_PyCV_test_task\Test_aerial_imagery").iterdir() if fn.is_dir()]:
            for tif in d.glob('*.tif'):
                new_fn = str(tif.with_suffix('.he.tif'))
                cv2.imwrite(new_fn, do_he(str(tif)))
                cp_proj(str(tif), new_fn)

if __name__ == '__main__':
    main()

