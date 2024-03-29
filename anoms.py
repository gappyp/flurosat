# default params (for interative or webapp)
CAN_L = 1379
CAN_U = 289
DIL_I = 55
BLUR = 20
THRESH_L = 55
THRUSH_U = 255

try:
    from pathlib import Path
except ImportError:
    pass

import argparse
import sys
import cv2
import numpy as np
from gdalcopyproj import cp_proj

def nothing(x):     # create trackbar requires this
    pass

def cmd_args():
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

    return args, fns

def main():
    args, fns = cmd_args()

    cv2.namedWindow('canny')
    cv2.createTrackbar('lower', 'canny', CAN_L, 10000, nothing)
    cv2.createTrackbar('upper', 'canny', CAN_U, 10000, nothing)

    cv2.namedWindow('dilate')
    cv2.createTrackbar('iters', 'dilate', DIL_I, 100, nothing)

    cv2.namedWindow('blur')
    cv2.createTrackbar('ss', 'blur', BLUR, 25, nothing)

    cv2.namedWindow('thresh1')
    cv2.createTrackbar('lower', 'thresh1', THRESH_L, 255, nothing)
    cv2.createTrackbar('upper', 'thresh1', THRUSH_U, 255, nothing)

    for fn in fns:
        img = cv2.imread(str(fn), cv2.IMREAD_GRAYSCALE)
        while(True):
            canny, dilate, blur, thresh1 = proc_img(img)

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

# arg can either by string (path) or ndarray (parsed image)
def proc_img(arg):
    if isinstance(arg, str):
        img = cv2.imread(str(fn), cv2.IMREAD_GRAYSCALE)
    else:
        img = arg

    if __name__ == "__main__":
        a1 = cv2.getTrackbarPos('lower', 'canny')
        a2 = cv2.getTrackbarPos('upper', 'canny')
        a3 = cv2.getTrackbarPos('iters', 'dilate')
        a4 = cv2.getTrackbarPos('ss', 'blur')
        a5 = cv2.getTrackbarPos('lower', 'thresh1')
        a6 = cv2.getTrackbarPos('upper', 'thresh1')
    else:
        a1, a2, a3, a4, a5, a6 = CAN_L, CAN_U, DIL_I, BLUR, THRESH_L, THRUSH_U

    canny = cv2.Canny(img, a1, a2)
    dilate = cv2.dilate(canny, kernel=None, iterations=a3)
    blur = np.copy(img)
    blur[dilate == 255] = 255
    blur = cv2.medianBlur(blur, 2*a4+1)
    ret, thresh1 = cv2.threshold(blur, a5, a6, cv2.THRESH_BINARY_INV)

    if __name__ == "__main__":
        return canny, dilate, blur, thresh1
    else:
        return thresh1


if __name__ == "__main__":
    main()