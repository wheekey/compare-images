import cv2
from sklearn.cluster import KMeans
from collections import Counter


class DominantColors:
    CLUSTERS = None
    IMAGE = None
    COLORS = None
    LABELS = None

    def __init__(self, image, clusters=3):
        self.CLUSTERS = clusters
        self.IMAGE = image

    def define_color_weight(self, counter):
        color_weights = {}
        sum_all_colors = sum(counter.values())

        for index, (key, value) in enumerate(counter.items()):
            color_weights.update({key: value / sum_all_colors * 100})

        return color_weights

    def dominantColors(self):
        # read image
        img = cv2.imread(self.IMAGE)

        # convert to rgb from bgr
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # reshaping to a list of pixels
        img = img.reshape((img.shape[0] * img.shape[1], 3))

        # save image after operations
        self.IMAGE = img

        # using k-means to cluster pixels
        kmeans = KMeans(n_clusters=self.CLUSTERS)
        kmeans.fit(img)

        # the cluster centers are our dominant colors.
        self.COLORS = kmeans.cluster_centers_

        # save labels
        self.LABELS = kmeans.labels_

        # returning after converting to integer from float
        return {"colors": self.COLORS.astype(int), "weights": self.define_color_weight(Counter(self.LABELS))}


# img = '/bighdd/1.jpg'
# clusters = 5
# dc = DominantColors(img, clusters)
# colors = dc.dominantColors()

# print(colors)
