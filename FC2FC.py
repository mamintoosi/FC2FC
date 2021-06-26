# -*- coding: utf-8 -*-
#
#    Copyright (C) 2021-2029 by
#    Mahmood Amintoosi <m.amintoosi@gmail.com>
#    All rights reserved.
#    BSD license.
"""Functions for converting a Fully Connected Layer to Fully Convolutional Layer in TF"""

import keras
from keras import layers
from keras import models
from keras import optimizers
import tensorflow as tf

def seq_model(inputSize):
    model = Sequential(name="seqModel")
    model.add(Conv2D(32, (3, 3), activation='relu',
                            input_shape=(inputSize, inputSize, 1), name="Conv1"))
    model.add(MaxPooling2D((2, 2), name="MaxPool1"))
    model.add(Conv2D(64, (3, 3), activation='relu', name="Conv2"))
    model.add(MaxPooling2D((2, 2), name="MaxPool2"))
    model.add(Conv2D(128, (3, 3), activation='relu', name="Conv3"))
    model.add(MaxPooling2D((2, 2), name="MaxPool3"))
    model.add(Flatten(name="Flatten1"))
    model.add(Dense(10, activation='softmax', name="Dense1"))
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

    fcn_model = Sequential(name="FullyConv")
    fcn_model.add(Conv2D(32, (3, 3), activation='relu',
                            input_shape=(inputSize[0], inputSize[1], 1), name="Conv1"))
    fcn_model.add(MaxPooling2D((2, 2), name="MaxPool1"))
    fcn_model.add(Conv2D(64, (3, 3), activation='relu', name="Conv2"))
    fcn_model.add(MaxPooling2D((2, 2), name="MaxPool2"))
    fcn_model.add(Conv2D(128, (3, 3), activation='relu', name="Conv3"))
    fcn_model.add(MaxPooling2D((2, 2), name="MaxPool3"))
    fcn_model.add(Conv2D(10, (1, 1), activation='sigmoid', name="lastConv"))
    # convModel.summary()
    fcn_model.load_weights(mdl,by_name=True)
    set_conv_weights(fcn_model,model)
    return fcn_model

