"""
* geojsons
"""

import numpy as np
import cv2
import sys
from coord_tf import to_geo
from geojson import Feature, Polygon, FeatureCollection, dumps
from pathlib import Path
import sys

for d in [fn for fn in Path(r"Anomaly_PyCV_test_task\Test_aerial_imagery").iterdir() if fn.is_dir()]:
        # try just on "C:\Users\gap\flurosat\Anomaly_PyCV_test_task\Test_aerial_imagery\20171218T000000_HIRAMS_PLN_msavi_" for now
        if d.name != '20171218T000000_HIRAMS_PLN_msavi_':
            pass
            #continue

        for tif in d.glob('*.anoms.tif'):
            fn = tif

            img = cv2.imread(str(fn),0)
            print(img.shape)
            #sys.exit()
            im2,contours,hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            features = []
            for cnt in contours:
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

                #sys.exit()

                """
                rect = cv2.minAreaRect(cnt)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                print(box)
                """

                #features.append(Feature(geometry=Polygon([[to_geo(fn,x,y), to_geo(fn,x+w,y), to_geo(fn,x+w,y+h), to_geo(fn,x,y+h), to_geo(fn,x,y)]])))
                features.append(Feature(geometry=Polygon([pnts])))

                #cv2.rectangle(img,(x,y),(x+w,y+h),255,2)

            fc = FeatureCollection(features)
            fc_str = dumps(fc)
            with open(str(fn.with_suffix('.json')), 'w') as fp:
                fp.write(fc_str)

            #cv2.imshow('boxes', img)
            #k = cv2.waitKey()

