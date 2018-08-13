import argparse
from pathlib import Path
import sys
import cv2
import numpy as np
from gdalcopyproj import cp_proj

parser = argparse.ArgumentParser(
description='Detect canopy anomolies',
)

parser.add_argument('-f', action="store", type=Path)

args = parser.parse_args()

if args.f == None:
    # batch mode on all .he.tif
    fns = []
    for d in [fn for fn in Path(r"Anomaly_PyCV_test_task\Test_aerial_imagery").iterdir() if fn.is_dir()]:
        for tif in d.glob('*.he.tif'):
            fns.append(tif)
else:
    assert args.f.is_file()
    fns = [args.f]

#sys.exit()

# ======================================================================================================================
def nothing(x):     # create trackbar requires this
    pass

cv2.namedWindow('canny')
cv2.createTrackbar('lower', 'canny', 1379, 10000, nothing)
cv2.createTrackbar('upper', 'canny', 289, 10000, nothing)

cv2.namedWindow('dilate')
cv2.createTrackbar('iters', 'dilate', 55, 100, nothing)

cv2.namedWindow('blur')
cv2.createTrackbar('ss', 'blur', 11, 25, nothing)

cv2.namedWindow('thresh1')
cv2.createTrackbar('lower', 'thresh1', 55, 255, nothing)
cv2.createTrackbar('upper', 'thresh1', 255, 255, nothing)

for fn in fns:
    img = cv2.imread(str(fn), cv2.IMREAD_GRAYSCALE)
    while(True):
        canny = cv2.Canny(img, cv2.getTrackbarPos('lower', 'canny'), cv2.getTrackbarPos('upper', 'canny'))

        dilate = cv2.dilate(canny, kernel=None, iterations=cv2.getTrackbarPos('iters', 'dilate'))

        blur = np.copy(img)
        blur[dilate == 255] = 255
        blur = cv2.medianBlur(blur, 2*cv2.getTrackbarPos('ss', 'blur')+1)

        ret, thresh1 = cv2.threshold(blur, cv2.getTrackbarPos('lower', 'thresh1'), cv2.getTrackbarPos('upper', 'thresh1'), cv2.THRESH_BINARY_INV)

        if args.f:
            # display images
            cv2.imshow('original', img)
            cv2.imshow('canny', canny)
            cv2.imshow('dilate', dilate)
            cv2.imshow('blur', blur)
            cv2.imshow('thresh1', thresh1)

            k = cv2.waitKey(100) & 0xFF
            if k == 27:   # hit escape to quit
                break
        else:
            # write out processed images
            new_fn = str(fn.with_suffix('.anoms.tif'))
            cv2.imwrite(new_fn, thresh1)
            cp_proj(str(fn), new_fn)
            break

cv2.destroyAllWindows()
