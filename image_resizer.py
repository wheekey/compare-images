import cv2



def resize(img_path, width):
    img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    # 1- width, 0 - height
    scale_percent = width / img.shape[1]  * 100 # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)
    # resize image
    resized = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)

    print('Resized Dimensions : ', resized.shape)

    '''
    cv2.imshow("Resized image", resized)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    '''
    cv2.imwrite(img_path, resized)

def get_image_width(img_path):
    img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
    return img.shape[1]