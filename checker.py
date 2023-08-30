import numpy as np
from PIL import Image
from tensorflow.keras.preprocessing import image

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

from keras.applications.vgg16 import VGG16
from sklearn.metrics.pairwise import cosine_similarity


class Checker:
    """
    This class is responsible for checking whether the user has won or not
    """

    vgg16 = None
    """
    The VGG16 model that is used to compute the similarity between images
    """

    def __init__(self, *args, **kwargs):
        """
        Here we load the model and the weights beforehand
        This is done to avoid loading the model and weights every time
        """

        self.vgg16 = VGG16(
            weights="imagenet",
            include_top=False,
            pooling="max",
            input_shape=(224, 224, 3),
        )

        for model_layer in self.vgg16.layers:
            model_layer.trainable = False

    def load_image(self, image_path):
        """
        process the image provided by resizing it to 224x224
        """

        input_image = Image.open(image_path).convert("RGB")
        resized_image = input_image.resize((224, 224))

        return resized_image

    def get_image_embeddings(self, object_image: image):
        """
        convert image into 3d array and add additional dimension for model input
        return embeddings of the given image
        """

        image_array = np.expand_dims(image.img_to_array(object_image), axis=0)
        image_embedding = self.vgg16.predict(image_array)

        return image_embedding

    def check(self, first_image: str, second_image: str):
        """
        Takes image array and computes its embedding using VGG16 model.
        return embedding of the image
        """

        first_image = self.load_image(first_image)
        second_image = self.load_image(second_image)

        first_image_vector = self.get_image_embeddings(first_image)
        second_image_vector = self.get_image_embeddings(second_image)

        similarity_score = cosine_similarity(
            first_image_vector, second_image_vector
        ).reshape(
            1,
        )
        return similarity_score
