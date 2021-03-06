#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 19:01:55 2016

@author: aitor
"""

from keras.models import Sequential, load_model
from keras.layers import Flatten, Dense, Dropout, Lambda, ELU
from keras.layers.convolutional import Convolution2D
from keras.layers.pooling import MaxPooling2D

# Based on:
#   75% NVIDIA's end-to-end paper: https://arxiv.org/pdf/1604.07316v1.pdf
#   25% Comma.ai research: https://github.com/commaai/research/blob/master/SelfSteering.md
def getNNModel(model_path=None, reg_lambda=0.0):

    from keras.callbacks import Callback
    class LossHistory(Callback):
        def on_train_begin(self, logs={}):
            self.losses = []

        def on_batch_end(self, batch, logs={}):
            self.losses.append(logs.get('loss'))

    if model_path:
        model = load_model(model_path)
    else:
        #
        # ch, width, height = 3, 200, 66
        #
        # # init='he_normal',
        # model = Sequential()
        # model.add(Lambda(lambda x: x / 127.5 - 1., input_shape=(ch, width, height), output_shape=(ch, width, height)))
        #
        # model.add(Convolution2D(32, 5, 5, border_mode='same', name='conv1', activation='relu'))
        # #model.add(MaxPooling2D((2,2), strides=(2,2)))
        # model.add(Dropout(0.25))
        #
        # model.add(Convolution2D(64, 3, 3, border_mode='same', name='conv4', activation='relu'))
        # #model.add(MaxPooling2D((2,2), strides=(2,2)))
        # model.add(Dropout(0.25))
        #
        # model.add(Convolution2D(128, 3, 3, border_mode='same', name='conv5', activation='relu'))
        # #model.add(MaxPooling2D((2,2), strides=(2,2)))
        # model.add(Dropout(0.5))
        #
        # model.add(Flatten())
        # model.add(Dropout(0.5))
        #
        # model.add(Dense(1024, name='dense_1', activation='relu'))
        # model.add(Dropout(0.5))
        #
        # model.add(Dense(1, name='output'))

        ch, width, height = 3, 200, 66

        model = Sequential()
        model.add(Lambda(lambda x: x / 127.5 - 1., input_shape=(ch, width, height), output_shape=(ch, width, height)))

        model.add(Convolution2D(24, 5, 5, subsample=(2, 2), border_mode='same', init='he_normal', name='conv1'))
        model.add(ELU())
        # model.add(MaxPooling2D((5,5)))

        model.add(Convolution2D(36, 5, 5, subsample=(2, 2), border_mode='same', init='he_normal', name='conv2'))
        model.add(ELU())
        # model.add(MaxPooling2D((2,2), strides=(2,2)))
        # model.add(MaxPooling2D((5,5)))

        model.add(Convolution2D(48, 5, 5, subsample=(2, 2), border_mode='same', init='he_normal', name='conv3'))
        model.add(ELU())
        # model.add(MaxPooling2D((2,2), strides=(2,2)))
        # model.add(MaxPooling2D((5,5)))

        model.add(Convolution2D(64, 3, 3, border_mode='same', init='he_normal', name='conv4'))
        model.add(ELU())
        # model.add(MaxPooling2D((2,2), strides=(2,2)))
        # model.add(MaxPooling2D((3,3)))

        model.add(Convolution2D(64, 3, 3, border_mode='same', init='he_normal', name='conv5'))
        # model.add(MaxPooling2D((2,2), strides=(2,2)))
        # model.add(MaxPooling2D((2,2)))

        model.add(Flatten())
        model.add(ELU())
        model.add(Dropout(0.2))

        model.add(Dense(100, init='he_normal', name='dense_1'))
        model.add(ELU())
        model.add(Dropout(0.5))
        model.add(Dense(50, init='he_normal', name='dense_2'))
        model.add(ELU())
        model.add(Dropout(0.5))
        model.add(Dense(10, init='he_normal', name='dense_3'))
        model.add(ELU())
        model.add(Dropout(0.5))
        model.add(Dense(1, init='he_normal', name='output'))

    return model, LossHistory
