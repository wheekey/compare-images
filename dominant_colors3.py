from colorthief import ColorThief
import time
import image_resizer




def get_dominant_colors(img_path):
    color_thief = ColorThief(img_path)
    # get the dominant color
    dominant_color = color_thief.get_color(quality=1)
    palette = color_thief.get_palette(color_count=5)

    print(palette)


file_name = "/bighdd/Downloads/vannaya.txt"
with open(file_name) as f:
    images = f.readlines()
    start_time = time.time()
    for image in images:
        try:
            image_resizer.resize(image.rstrip(), 100)
            print("--- %s resized ---" % (image))
        except:
            print("Не смогли сресайзить")
    print("--- %s seconds ---" % (time.time() - start_time))
