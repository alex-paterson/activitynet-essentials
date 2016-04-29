import matplotlib.pyplot as plt
from skimage import data, color, exposure
from skimage.feature import hog

class ImageHelper:
    @staticmethod
    def show_hog(image):
        image = color.rgb2gray(image)
        imgplot = plt.imshow(image, cmap=plt.cm.gray)
        fd, hog_image = hog(image, orientations=8, pixels_per_cell=(16, 16),
            cells_per_block=(1, 1), visualise=True)
        hog_image_rescaled = exposure.rescale_intensity(hog_image,
            in_range=(0, 0.02))
        imgplot = plt.imshow(hog_image_rescaled, cmap=plt.cm.gray)
        plt.show()

    @staticmethod
    def get_hog(image):
        image = color.rgb2gray(image)
        imgplot = plt.imshow(image, cmap=plt.cm.gray)
        fd, hog_image = hog(image, orientations=8, pixels_per_cell=(16, 16),
            cells_per_block=(1, 1), visualise=True)
        hog_image_rescaled = exposure.rescale_intensity(hog_image,
            in_range=(0, 0.02))
        imgplot = plt.imshow(hog_image_rescaled, cmap=plt.cm.gray)
        plt.show()
