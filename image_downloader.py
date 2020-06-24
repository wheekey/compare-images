from comparison_results_repository import get_comparison_results
import urllib.request
from dotenv import load_dotenv
import os
import image_cropper
load_dotenv()

def download_competitor_images(comparison_results):
    for row in comparison_results:
        try:
            url = 'http://94.130.73.202:81/images/competitors/' + row['competitorLogin'] + '/' + row['parsedImageFilename']
            images_dir = os.getenv('APP_DIR') + os.getenv('COMPETITOR_IMAGES_DIR')
            image_full_path = images_dir + '/' + row['parsedImageFilename']

            generate_folder(images_dir)
            urllib.request.urlretrieve(url, image_full_path)
            #image_cropper.remove_white_background(image_full_path)
            print("downloaded image= ", url)
        except:
            print('An error occured.')

def download_pdlx_images(comparison_results):
    for row in comparison_results:
        try:
            url = 'http://94.130.73.202:81/images/pdlx/' + row[
                'ourImageFilename']
            images_dir = os.getenv('APP_DIR') + os.getenv('PDLX_IMAGES_DIR')
            image_full_path = images_dir + '/' + row['ourImageFilename']

            generate_folder(images_dir)
            urllib.request.urlretrieve(url, image_full_path)
            #image_cropper.remove_white_background(image_full_path)
            print("downloaded image= ", url)
        except:
            print('An error occured.')

def generate_folder(dir):
    if not os.path.isdir(dir):
        os.makedirs(dir)

comparison_results = get_comparison_results()
download_pdlx_images(comparison_results)
download_competitor_images(comparison_results)


