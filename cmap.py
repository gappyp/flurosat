"""
* applies the color map features in Anomaly_PyCV_test_task/Screenshot 2018-08-10 00.55.26_labelled.png to .he.tif images
"""

from pathlib import Path
import cv2
import numpy as np
import sys
import matplotlib.pyplot as plt
from gdalcopyproj import cp_proj

# get color map

cmap = cv2.imread(str(r"Anomaly_PyCV_test_task\Screenshot 2018-08-10 00.55.26_labelled.png"), cv2.IMREAD_COLOR);      # BGR color image
lut = np.zeros((256, 1, 3), dtype=np.uint8)
ramp_bnds = (388, 869)
row       = 1357
for i in range(3):
    samps = cmap[row, ramp_bnds[0]:ramp_bnds[1], i]      # more sample points, so downsample
    idx = [256*i for i in range(ramp_bnds[1]-ramp_bnds[0])]
    lin_int = np.interp(np.arange(0, idx[-1], 1, int), idx, samps)
    rs = (np.mean(lin_int.reshape(-1, ramp_bnds[1]-ramp_bnds[0]-1), 1)).astype(np.uint8)
    plt.plot(rs)
    lut[:, 0, i] = rs
    # it's interesting to see the map with matplotlib :D

for d in [fn for fn in Path(r"Anomaly_PyCV_test_task\Test_aerial_imagery").iterdir() if fn.is_dir()]:
    for tif in d.glob('*.he.tif'):
        im = cv2.imread(str(tif), cv2.IMREAD_GRAYSCALE);
        im = cv2.cvtColor(im, cv2.COLOR_GRAY2BGR);
        im = cv2.LUT(im, lut)

        #cv2.imshow("im", im);
        #cv2.waitKey(0);
        new_fn = str(tif.with_suffix('.color.tif'))
        cv2.imwrite(new_fn, im)
        cp_proj(str(tif), new_fn)