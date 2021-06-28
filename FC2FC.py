# -*- coding: utf-8 -*-
#
#    Copyright (C) 2021-2029 by
#    Mahmood Amintoosi <m.amintoosi@gmail.com>
#    All rights reserved.
#    MIT license.
"""Functions for converting a Fully Connected Layer to Fully Convolutional Layer in TF"""

# The main idea is borrowed from: https://learnopencv.com/cnn-fully-convolutional-image-classification-with-tensorflow/

import keras
from keras import layers
from keras import models
from keras import optimizers
# This is module with image preprocessing utilities
import tensorflow as tf
from keras.layers import *


def seq_model(inputSize):
    model = models.Sequential()
    model.add(layers.Conv2D(32, (3, 3), activation='relu', name="Conv1",
                            input_shape=(inputSize, inputSize, 3)))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(64, (3, 3), activation='relu', name="Conv2"))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(128, (3, 3), activation='relu', name="Conv3"))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(128, (3, 3), activation='relu', name="Conv4"))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Conv2D(256, (3, 3), activation='relu', name="Conv5"))
    model.add(layers.Conv2D(512, (3, 3), activation='relu', name="Conv6"))
    model.add(layers.MaxPooling2D((2, 2)))
    model.add(layers.Flatten())
    model.add(layers.Dense(1, activation='sigmoid'))
    return model

# setting FC weights to the final convolutional layer
def set_conv_weights(conv_model, feature_extractor):
    # get pre-trained ResNet50 FC weights
    dense_layer_weights = feature_extractor.layers[-1].get_weights()
    weights_list = [
        tf.reshape(
            dense_layer_weights[0], (1, 1, *dense_layer_weights[0].shape),
        ).numpy(),
        dense_layer_weights[1],
    ]
    conv_model.get_layer(name="lastConv").set_weights(weights_list)

# Convert Model
def convert_model(model,mdl,inputSize):
    """
    Convert FC2FC

    Parameters
    ----------
    model : input model
    mdl: model
    inputSize: the size of input image 

    Returns
    -------
    converted model

    """    
    convModel = models.Sequential(name="FullyConv")
    convModel.add(layers.Conv2D(32, (3, 3), activation='relu',
                            input_shape=(inputSize[0], inputSize[1], 3), name="Conv1"))
    convModel.add(layers.MaxPooling2D((2, 2), name="MaxPool1"))
    convModel.add(layers.Conv2D(64, (3, 3), activation='relu', name="Conv2"))
    convModel.add(layers.MaxPooling2D((2, 2), name="MaxPool2"))
    convModel.add(layers.Conv2D(128, (3, 3), activation='relu', name="Conv3"))
    convModel.add(layers.MaxPooling2D((2, 2), name="MaxPool3"))
    convModel.add(layers.Conv2D(128, (3, 3), activation='relu', name="Conv4"))
    convModel.add(layers.MaxPooling2D((2, 2), name="MaxPool4"))
    convModel.add(layers.Conv2D(256, (3, 3), activation='relu', name="Conv5"))
    convModel.add(layers.Conv2D(512, (3, 3), activation='relu', name="Conv6"))
    convModel.add(layers.MaxPooling2D((2, 2), name="MaxPool5"))
    convModel.add(layers.Conv2D(1, (1, 1), activation='sigmoid', name="lastConv"))

    convModel.load_weights(mdl,by_name=True)
    set_conv_weights(convModel,model)
    return convModel

def seq_model_hoda(inputSize):
    model = models.Sequential(name="seqModel")
    model.add(layers.Conv2D(32, (3, 3), activation='relu',
                            input_shape=(inputSize, inputSize, 1), name="Conv1"))
    model.add(layers.MaxPooling2D((2, 2), name="MaxPool1"))
    model.add(layers.Conv2D(64, (3, 3), activation='relu', name="Conv2"))
    model.add(layers.MaxPooling2D((2, 2), name="MaxPool2"))
    model.add(layers.Conv2D(128, (3, 3), activation='relu', name="Conv3"))
    model.add(layers.MaxPooling2D((2, 2), name="MaxPool3"))
    model.add(layers.Flatten(name="Flatten1"))
    model.add(layers.Dense(10, activation='softmax', name="Dense1"))
    return model

# Convert Model
def convert_model_hoda(model,mdl,inputSize):
    """
    Convert FC2FC for Hoda dataset

    Parameters
    ----------
    model : input model
    mdl: model
    inputSize: the size of input image 

    Returns
    -------
    converted model

    """    

    convModel = models.Sequential(name="FullyConv")
    convModel.add(layers.Conv2D(32, (3, 3), activation='relu',
                            input_shape=(inputSize[0], inputSize[1], 1), name="Conv1"))
    convModel.add(layers.MaxPooling2D((2, 2), name="MaxPool1"))
    convModel.add(layers.Conv2D(64, (3, 3), activation='relu', name="Conv2"))
    convModel.add(layers.MaxPooling2D((2, 2), name="MaxPool2"))
    convModel.add(layers.Conv2D(128, (3, 3), activation='relu', name="Conv3"))
    convModel.add(layers.MaxPooling2D((2, 2), name="MaxPool3"))
    convModel.add(layers.Conv2D(10, (1, 1), activation='sigmoid', name="lastConv"))
    # convModel.summary()
    convModel.load_weights(mdl,by_name=True)
    set_conv_weights(convModel,model)
    return convModel

