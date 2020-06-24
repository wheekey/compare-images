from flask import Flask, render_template
import comparison_results_repository
import pandas as pd
import image_comparison_sift
import image_comparison_surf
import image_comparison_hash
import image_comparison_avg_color
from dotenv import load_dotenv
import os
import cv2
import image_resizer
import image_cropper
import colorsys

load_dotenv()

app = Flask(__name__)


@app.route("/")
def hello():
    comparison_results = comparison_results_repository.get_comparison_results()
    pd.set_option('max_colwidth', 500)
    # http://94.130.73.202:81/images/pdlx/
    added_comparison_result = []

    for result in comparison_results:
        try:
            result['imgPdlxPath'] = 'http://94.130.73.202:81/images/pdlx/' + result['ourImageFilename']
            result['imgCompetitorPath'] = 'http://94.130.73.202:81/images/competitors/' + result[
                'competitorLogin'] + "/" + \
                                          result['parsedImageFilename']
            img_pdlx_path = os.getenv('APP_DIR') + os.getenv('PDLX_IMAGES_DIR') + '/' + result['ourImageFilename']
            img_competitor_path = os.getenv('APP_DIR') + os.getenv('COMPETITOR_IMAGES_DIR') + '/' + result[
                'parsedImageFilename']

            loaded_pdlx_image = load_image(img_pdlx_path)
            # image_resizer.resize(img_competitor_path, image_resizer.get_image_width(img_pdlx_path))
            # image_cropper.crop_image(img_competitor_path, loaded_pdlx_image.shape[1], loaded_pdlx_image.shape[0])
            loaded_competitor_image = load_image(img_competitor_path)

            result['siftResult'] = image_comparison_sift.compare(loaded_pdlx_image, loaded_competitor_image)
            result['surfResult'] = image_comparison_surf.compare(loaded_pdlx_image, loaded_competitor_image)
            # result['avgColorPDLX'] = image_comparison_avg_color.get_avg_color(img_pdlx_path)
            # result['avgColorCompetitor'] = image_comparison_avg_color.get_avg_color(img_competitor_path)
            avgColorMiddlePDLX = image_comparison_avg_color.get_avg_color_middle_of_the_img(img_pdlx_path, 5)
            avgColorMiddleCompetitor = image_comparison_avg_color.get_avg_color_middle_of_the_img(img_competitor_path,
                                                                                                  5)
            avgColorMiddlePDLX2 = image_comparison_avg_color.get_avg_color_middle_of_the_img(img_pdlx_path, 15)
            avgColorMiddleCompetitor2 = image_comparison_avg_color.get_avg_color_middle_of_the_img(img_competitor_path,
                                                                                                   15)

            avgColorMiddlePDLX3 = image_comparison_avg_color.get_avg_color_middle_of_the_img(img_pdlx_path, 30)
            avgColorMiddleCompetitor3 = image_comparison_avg_color.get_avg_color_middle_of_the_img(img_competitor_path,
                                                                                                   30)

            result['hsvPDLX'] = colorsys.rgb_to_hsv(avgColorMiddlePDLX[0], avgColorMiddlePDLX[1], avgColorMiddlePDLX[2])
            result['hsvCompetitor'] = colorsys.rgb_to_hsv(avgColorMiddleCompetitor[0], avgColorMiddleCompetitor[1],
                                                          avgColorMiddleCompetitor[2])

            result['hsvPDLX2'] = colorsys.rgb_to_hsv(avgColorMiddlePDLX2[0], avgColorMiddlePDLX2[1],
                                                     avgColorMiddlePDLX2[2])
            result['hsvCompetitor2'] = colorsys.rgb_to_hsv(avgColorMiddleCompetitor2[0], avgColorMiddleCompetitor2[1],
                                                           avgColorMiddleCompetitor2[2])

            result['hsvPDLX3'] = colorsys.rgb_to_hsv(avgColorMiddlePDLX3[0], avgColorMiddlePDLX3[1],
                                                     avgColorMiddlePDLX3[2])
            result['hsvCompetitor3'] = colorsys.rgb_to_hsv(avgColorMiddleCompetitor3[0], avgColorMiddleCompetitor3[1],
                                                           avgColorMiddleCompetitor3[2])

            result['avgColorIndex'] = get_avg_color_index(result['hsvPDLX'], result['hsvCompetitor'])
            result['avgColorIndex2'] = get_avg_color_index(result['hsvPDLX2'], result['hsvCompetitor2'])
            result['avgColorIndex3'] = get_avg_color_index(result['hsvPDLX3'], result['hsvCompetitor3'])

            # Условно определим вес фильтра
            result['hash'] = image_comparison_hash.compare(img_pdlx_path, img_competitor_path)

            # Занизим индекс, если avgColorIndex2 слишком велик
            if result['avgColorIndex2'] > 35:
                result['siftResult'] = 5
        except:
            print("error")


    df = pd.DataFrame(comparison_results)
    df.sort_values(['siftResult', 'avgColorIndex', 'avgColorIndex2', 'hash'], ascending=[False, True, True, True],
                   inplace=True)
    df.to_html('templates/results.html',
               formatters={'imgPdlxPath': path_to_image_html, 'imgCompetitorPath': path_to_image_html}, escape=False)

    return render_template('results.html')


def get_avg_color_index(hsv1, hsv2):
    return (abs(hsv1[0] - hsv2[0]) * 100) + (abs(hsv1[1] - hsv2[1]) * 100) + (abs(hsv1[2] - hsv2[2]) * 100 / 255)


def load_image(img_path):
    return cv2.imread(img_path)


def path_to_image_html(path):
    return '<img src="' + path + '" width="400" >'


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5002, debug=True)
