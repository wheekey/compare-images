import cv2
import numpy

def get_avg_color(image):
    # https://stackoverflow.com/questions/43111029/how-to-find-the-average-colour-of-an-image-in-python-with-opencv
    img = cv2.imread(image)

    avg_color_per_row = numpy.average(img, axis=0)
    avg_color = numpy.average(avg_color_per_row, axis=0)
    return avg_color

def get_avg_color_middle_of_the_img(image, cropped_size_percentage):
    cropped_img = get_middle_of_the_img(image, cropped_size_percentage)

    avg_color_per_row = numpy.average(cropped_img, axis=0)
    avg_color = numpy.average(avg_color_per_row, axis=0)
    return avg_color

def get_middle_of_the_img(image, cropped_size_percentage):
    img = cv2.imread(image)

    h_orig, w_orig, channels = img.shape

    # Сколько нужно ширины и высоты
    h = int(h_orig * cropped_size_percentage / 100)
    w = int(w_orig * cropped_size_percentage / 100)

    x = int(w_orig / 2) - int(w / 2)
    y = int(h_orig / 2) - int(h / 2)

    return img[y:y + h, x:x + w]