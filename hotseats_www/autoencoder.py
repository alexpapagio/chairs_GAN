import os
import requests
import tensorflow as tf
import tensorflow
from tensorflow import keras
from tensorflow.keras.layers import Dense, Lambda
from tensorflow.keras import backend as K

AE_MODEL_DECODER_URL = "https://storage.googleapis.com/chairs-gan-images/autoencoder-models/hotseats-6k-autoencoder_decoder.keras"
AE_MODEL_ENCODER_URL = "https://storage.googleapis.com/chairs-gan-images/autoencoder-models/hotseats-6k-autoencoder_encoder_vae_woK.keras"


def download_file(url, output_path):
    """
    Download a file from the given URL.
    """

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
    # url = AE_MODEL_ENCODER_URL
    # model_path = os.path.basename(url)
    # download_file(url, model_path)
    # model = keras.models.load_model(
    #     model_path,
    #     custom_objects={
    #         "tensorflow": tensorflow,
    #         # "z": z_function,
    #         # "sampling": sampling,
    #     },
    #     safe_mode=False,
    # )
    # return model
    return encoder_build_and_restore_weights()


# do not cache this because the models are not thread-safe
# https://docs.streamlit.io/library/api-reference/performance/st.cache_resource
# https://docs.streamlit.io/library/advanced-features/caching#deciding-which-caching-decorator-to-use
# downloading the file once and reusing it already "caches" the download step
def decoder_model():
    """
    Load the pre-trained decoder model.
    """
    url = AE_MODEL_DECODER_URL
    model_path = os.path.basename(url)
    download_file(url, model_path)
    model = keras.models.load_model(model_path)
    return model


# def sampling(args):
#     """Reparametrization trick z-mu +sigma +epsilon"""
#     z_mean, z_log_var = args
#     batch = tf.shape(z_mean)[0]
#     dim = tf.shape(z_mean)[1]
#     epsilon = K.random_normal(shape=(batch, dim))
#     return z_mean + K.exp(0.5 * z_log_var) * epsilon


# def z_function(inputs):
#     encoding_dim = 200
#     z_mean = Dense(encoding_dim, name="z_mean")(inputs)
#     z_log_var = Dense(encoding_dim, name="z_log_var")(inputs)
#     z = Lambda(sampling, output_shape=(encoding_dim,), name="z")([z_mean, z_log_var])
#     return z


import tensorflow as tf
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
    decoded = Conv2D(1, (3, 3), activation="sigmoid", padding="same")(
        x
    )  # Change padding to 'same'
    return Model(input_encoded, decoded)


def encoder_build_and_restore_weights():
    # Define input shape and encoding dimension
    input_shape = (100, 100, 1)
    encoding_dim = 200  # Example encoding dimension

    # initialise encoder model
    encoder_vae = build_encoder_vae(input_shape, encoding_dim)
    return encoder_vae

    # restore weights from saved json
    # encoder_vae.load_weights("decoder_weights.h5")


def decoder_build_and_restore_weights():
    # Define input shape and encoding dimension
    input_shape = (100, 100, 1)
    encoding_dim = 200  # Example encoding dimension

    # initialise decoder model
    decoder_vae = build_decoder_vae(encoding_dim, input_shape)
    return decoder_vae

    # restore weights from saved json
    # decoder_vae.load_weights("decoder_weights.h5")
