# -*- coding: utf-8 -*-
#
#    Copyright (C) 2021-2029 by
#    Mahmood Amintoosi <m.amintoosi@gmail.com>
#    All rights reserved.
#    BSD license.
"""Functions for converting a Fully Connected Layer to Fully Convolutional Layer in TF"""


# Convert Model
def buildModel(model,mdl,inputSize):
    """
    Incomplete....
    Convert FC2FC

    Parameters
    ----------
    model : input model
    mdl: model

    Returns
    -------
    converted model

    Notes
    -----
    
    """    

    fcn_model = Sequential(name="hodaFCN")
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
