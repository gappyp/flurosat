"""
* geojsons
"""

import numpy as np
import cv2
import sys
from coord_tf import to_geo
from geojson import Feature, Polygon, FeatureCollection, dumps
from pathlib import Path

for d in [fn for fn in Path(r"Anomaly_PyCV_test_task\Test_aerial_imagery").iterdir() if fn.is_dir()]:
        for tif in d.glob('*.anoms.tif'):
            fn = tif

            img = cv2.imread(str(fn),0)
            im2,contours,hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            features = []
            for cnt in contours:
                x,y,w,h = cv2.boundingRect(cnt)

                """
                rect = cv2.minAreaRect(cnt)
                box = cv2.boxPoints(rect)
                box = np.int0(box)
                print(box)
                """

                features.append(Feature(geometry=Polygon([[to_geo(fn,x,y), to_geo(fn,x+w,y), to_geo(fn,x+w,y+h), to_geo(fn,x,y+h), to_geo(fn,x,y)]])))

                #cv2.rectangle(img,(x,y),(x+w,y+h),255,2)

            fc = FeatureCollection(features)
            fc_str = dumps(fc)
            with open(str(fn.with_suffix('.json')), 'w') as fp:
                fp.write(fc_str)

            #cv2.imshow('boxes', img)
            #k = cv2.waitKey()

