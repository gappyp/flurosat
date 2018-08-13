"""
* get histogram equalization of images (images other than ccci have very little contrast)
* should only be run once
"""

import cv2
from pathlib import Path
import sys
from gdalcopyproj import cp_proj        # this used to copy geotiff meta data into processed files

for d in [fn for fn in Path(r"Anomaly_PyCV_test_task\Test_aerial_imagery").iterdir() if fn.is_dir()]:
        for tif in d.glob('*.tif'):
            grey = cv2.imread(str(tif), 0)
            grey_eq = cv2.equalizeHist(grey)

            # remove black background while here too
            height, width = grey_eq.shape
            corners = [(0,0), (width-1,height-1), (width-1,0), (0,height-1)]
            for corner in corners:
                cv2.floodFill(grey_eq, mask=None, seedPoint=corner, newVal=255);

            new_fn = str(tif.with_suffix('.he.tif'))
            cv2.imwrite(new_fn, grey_eq)
            cp_proj(str(tif), new_fn)