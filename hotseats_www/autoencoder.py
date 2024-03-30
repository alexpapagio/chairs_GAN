import os
import requests

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import (
    Input,
    Conv2D,
    MaxPooling2D,
    UpSampling2D,
    Flatten,
    Reshape,
    Dense,
    ZeroPadding2D,
    Lambda,
)
from tensorflow.keras.models import Model
from tensorflow.keras.losses import binary_crossentropy
from tensorflow.keras import backend as K

AE_MODEL_DECODER_WEIGHTS_URL = "https://storage.googleapis.com/chairs-gan-images/autoencoder-models/hotseats-6k-autoencoder_decoder.h5"
AE_MODEL_ENCODER_WEIGHTS_URL = "https://storage.googleapis.com/chairs-gan-images/autoencoder-models/hotseats-6k-autoencoder_encoder_vae_woK.h5"


def download_file(url, output_path):
    """
    Download a file from the given URL.
    """

    if os.path.exists(output_path):
        return

    response = requests.get(url, timeout=10)
    response.raise_for_status()
    with open(output_path, "wb") as f:
        f.write(response.content)


# do not cache this because the models are not thread-safe
# https://docs.streamlit.io/library/api-reference/performance/st.cache_resource
# https://docs.streamlit.io/library/advanced-features/caching#deciding-which-caching-decorator-to-use
# downloading the file once and reusing it already "caches" the download step
def encoder_model():
    """
    Load the pre-trained encoder model.
    """
    # Define input shape and encoding dimension
    input_shape = (100, 100, 3)
    encoding_dim = 100  # Example encoding dimension

    # initialise encoder model
    encoder = build_encoder_vae(input_shape, encoding_dim)

    # restore weights from saved json
    download_file(AE_MODEL_ENCODER_WEIGHTS_URL, "encoder_weights.h5")
    encoder.load_weights("encoder_weights.h5")
    return encoder


# do not cache this because the models are not thread-safe
# https://docs.streamlit.io/library/api-reference/performance/st.cache_resource
# https://docs.streamlit.io/library/advanced-features/caching#deciding-which-caching-decorator-to-use
# downloading the file once and reusing it already "caches" the download step
def decoder_model():
    """
    Load the pre-trained decoder model.
    """
    # Define input shape and encoding dimension
    input_shape = (100, 100, 3)
    encoding_dim = 100  # Example encoding dimension

    # initialise decoder model
    decoder = build_decoder_vae(encoding_dim, input_shape)

    # restore weights from saved json
    download_file(AE_MODEL_DECODER_WEIGHTS_URL, "decoder_weights.h5")
    decoder.load_weights("decoder_weights.h5")
    return decoder


def sampling(args):
    """Reparametrization trick z-mu +sigma +epsilon"""
    z_mean, z_log_var = args
    batch = tf.shape(z_mean)[0]
    dim = tf.shape(z_mean)[1]
    epsilon = K.random_normal(shape=(batch, dim))
    return z_mean + K.exp(0.5 * z_log_var) * epsilon


def build_encoder_vae(input_shape, encoding_dim):
    input_img = Input(shape=input_shape)
    x = Conv2D(32, (3, 3), activation="relu", padding="same")(input_img)
    x = MaxPooling2D((2, 2), padding="same")(x)
    x = Conv2D(64, (3, 3), activation="relu", padding="same")(x)
    x = MaxPooling2D((2, 2), padding="same")(x)
    x = Conv2D(128, (3, 3), activation="relu", padding="same")(x)
    x = MaxPooling2D((2, 2), padding="same")(x)
    flattened = Flatten()(x)
    z_mean = Dense(encoding_dim, name="z_mean")(flattened)
    z_log_var = Dense(encoding_dim, name="z_log_var")(flattened)
    z = Lambda(sampling, output_shape=(encoding_dim,), name="z")([z_mean, z_log_var])
    return Model(input_img, [z_mean, z_log_var, z])


def build_decoder_vae(encoded_dim, input_shape):
    input_encoded = Input(shape=(encoded_dim,))
    x = Dense(12 * 12 * 128, activation="relu")(
        input_encoded
    )  # Calculate the number of neurons to match the desired shape
    x = Reshape((12, 12, 128))(
        x
    )  # Reshape to match the shape after the last pooling layer in the encoder
    x = Conv2D(128, (3, 3), activation="relu", padding="same")(x)
    x = UpSampling2D((2, 2))(x)
    x = Conv2D(64, (3, 3), activation="relu", padding="same")(x)
    x = UpSampling2D((2, 2))(x)
    x = Conv2D(32, (3, 3), activation="relu", padding="same")(
        x
    )  # Change padding to 'same'
    x = UpSampling2D((2, 2))(x)
    x = ZeroPadding2D(2)(x)
    decoded = Conv2D(3, (3, 3), activation="sigmoid", padding="same")(
        x
    )  # Change padding to 'same'
    return Model(input_encoded, decoded)


def interpolate_latent_vectors(encoding1, encoding2, steps=10):
    # Interpolate between the encodings
    interpolated_encodings = []
    for i in range(steps):
        alpha = i / steps
        interpolated_encoding = alpha * encoding2 + (1 - alpha) * encoding1
        interpolated_encodings.append(interpolated_encoding)
    return interpolated_encodings
