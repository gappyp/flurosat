import cv2
import sys
import matplotlib.pyplot as plt
import numpy as np

image = cv2.imread('mask_test.png', cv2.IMREAD_GRAYSCALE)
mask = cv2.imread('mask.png', cv2.IMREAD_GRAYSCALE)

blurred_image = cv2.GaussianBlur(image, (7, 7), 0)
plt.imshow(blurred_image, cmap='gray')

blurred_mask = cv2.GaussianBlur(mask, (7, 7), 0)
#plt.figure()
#plt.imshow(blurred_mask, cmap='gray')

result = (blurred_image / blurred_mask)*255
# replace nans with 0
result[result == np.nan] = 0.0
# convert back to integers
result = result.astype(np.uint8)

plt.figure()
plt.imshow(result, cmap='gray')

plt.show()