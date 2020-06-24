from numpy import ndenumerate

from dominant_colors4 import DominantColors
import time
import copy
import parsing_houzz_repository
import json


def form_result_dict(colors):
    result = []

    index = 0
    for color in colors["colors"]:
        element = {}
        element["color"] = color.tolist()
        element["weight"] = colors["weights"][index]
        result.append(element)
        index = index + 1

    return result



files = ["/bighdd/Downloads/colorpalettes.txt",]

default_image_colors_dict =  {
  "status": "ok",
  "error": [],
  "method": "extract_image_colors",
  "result": [

  ]
}
clusters = 5


for file in files:
    with open(file) as f:
        images = f.readlines()
        start_time = time.time()
        for image in images:
            try:
                dc = DominantColors(image.rstrip(), clusters)
                colors = dc.dominantColors()
                dict = copy.deepcopy(default_image_colors_dict)
                dict["result"] = form_result_dict(colors)
                row = {}
                row["imgCategory"] = file
                row["imgFilename"] = image
                row["imageColors"] = json.dumps(dict)
                parsing_houzz_repository.save(row)
                print("Сохранили %s" % dict)
            except Exception as e:
                print("Не смогли Сохранить цвета" + str(e))





