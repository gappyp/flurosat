from __future__ import print_function

try:
    from pathlib import Path
except ImportError:
    pass

import numpy as np
import cv2
import sys
from coord_tf import to_geo
from geojson import Feature, Polygon, FeatureCollection, dumps
import sys
import shapefile
import zipfile

cv_vers = int(cv2.__version__.split('.')[0])

# again arg can be file or ndarray
# fn needed for transformation
def get_sf(arg, fn):
    if isinstance(arg, str):
        img = cv2.imread(arg,0)
    else:           # TODO: should be elif ndarray (confirm)
        img = arg

    #print(img.shape)
    #sys.exit()
    # https://stackoverflow.com/questions/40278444/error-using-cv2-findcontours-with-python (previous python 3 version returned 3 vals sighhhh)
    if cv_vers is 3:
        im2,contours,hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    else:
        contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    features = []

    w = shapefile.Writer(shapefile.POLYGON)
    w.field('FIRST_FLD','C','40')
    w.field('SECOND_FLD','C','40')

    for i, cnt in enumerate(contours):
        temp = np.zeros(img.shape, dtype=img.dtype)
        #x,y,w,h = cv2.boundingRect(cnt)

        epsilon = 0.001*cv2.arcLength(cnt,True)         # TODO: maybe try error as

        approx = cv2.approxPolyDP(cnt,epsilon,True)
        #cv2.drawContours(temp,approx,-1,255,3)
        #cv2.imshow('outline', temp)
        #cv2.waitKey(0)

        pnts = []
        for pnt in approx:
            x, y = pnt[0]
            #print(x,y)
            pnts.append(to_geo(fn, x, y))
        # add the laast one to close poly
        x, y = approx[0][0]
        pnts.append(to_geo(fn, x, y))

        #features.append(Feature(geometry=Polygon([[to_geo(fn,x,y), to_geo(fn,x+w,y), to_geo(fn,x+w,y+h), to_geo(fn,x,y+h), to_geo(fn,x,y)]])))
        #features.append(Feature(geometry=Polygon([pnts])))
        w.poly(parts=[pnts])
        w.record(str(i),'Polygon')

    w.save('shapefile')
    z = zipfile.ZipFile("shapefile.zip", "w")
    z.write('shapefile.shp')
    z.write('shapefile.dbf')
    z.write('shapefile.shx')
    z.close()

    return None

    #cv2.imshow('boxes', img)
    #k = cv2.waitKey()


def main():
    for d in [fn for fn in Path(r"Anomaly_PyCV_test_task\Test_aerial_imagery").iterdir() if fn.is_dir()]:
            for tif in d.glob('*.anoms.tif'):
                fn = tif

                fc_str = get_gj(str(fn), str(fn))

                with open(str(fn.with_suffix('.json')), 'w') as fp:
                    fp.write(fc_str)

                #cv2.imshow('boxes', img)
                #k = cv2.waitKey()

if __name__ == "__main__":
    test_fn = r"C:\Users\gap\flurosat\Anomaly_PyCV_test_task\Test_aerial_imagery\20171218T000000_HIRAMS_PLN_msavi_\20171218T000000_HIRAMS_PLN_ccci_gray.he.anoms.tif"
    get_gj(test_fn, test_fn)

    #main()