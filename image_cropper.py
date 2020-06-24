from skimage import io, img_as_float
import numpy as np
import cv2

def remove_white_background(file_path):
    try:
        image = img_as_float(io.imread(file_path))

        # Select all pixels almost equal to white
        # (almost, because there are some edge effects in jpegs
        # so the boundaries may not be exactly white)
        white = np.array([1, 1, 1])
        mask = np.abs(image - white).sum(axis=2) < 0.05

        # Find the bounding box of those pixels
        coords = np.array(np.nonzero(~mask))
        top_left = np.min(coords, axis=1)
        bottom_right = np.max(coords, axis=1)

        out = image[top_left[0]:bottom_right[0],
                    top_left[1]:bottom_right[1]]

        io.imsave(file_path, out)
    except:
        print('Cropping error occured.')

def crop_image(img_path, w, h):
    img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    y = 0
    x = 0
    crop_img = img[y:y + h, x:x + w]
    print("Cropped image ", img_path)
    '''
    cv2.imshow("cropped", crop_img)
    cv2.waitKey(0)
    '''
    cv2.imwrite(img_path, crop_img)
