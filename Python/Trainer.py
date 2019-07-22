from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Input, Activation, Conv2D, Dense, Flatten, MaxPooling2D


class Trainer:
    def __init__(self):
        train_datagen = ImageDataGenerator(rescale=1./255,
                                           shear_range=0.2,
                                           zoom_range=0.2,
                                           horizontal_flip=True)

        validate_datagen = ImageDataGenerator(rescale=1./255)

        self.train_set = train_datagen.flow_from_directory('data/train',
                                                           target_size=(
                                                               24, 24),
                                                           batch_size=32,
                                                           color_mode="grayscale",
                                                           class_mode='binary')

        self.validate_set = validate_datagen.flow_from_directory('data/validate',
                                                                 target_size=(
                                                                     24, 24),
                                                                 batch_size=32,
                                                                 color_mode="grayscale",
                                                                 class_mode='binary')

        self.model = Sequential()
        self.model.add(Conv2D(16, kernel_size=3,
                              padding='same', activation='relu', input_shape=(24, 24, 1)))
        self.model.add(MaxPooling2D(pool_size=2))

        # self.model.add(Conv2D(64, kernel_size=3, strides=1,
        #                       padding='same', activation='relu'))
        # self.model.add(MaxPooling2D(pool_size=2))

        self.model.add(Flatten())

        self.model.add(Dense(128))
        self.model.add(Activation('relu'))

        self.model.add(Dense(1))
        self.model.add(Activation('sigmoid'))

        self.model.compile(
            optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

        self.model.summary()

    def train(self, path):
        self.model.fit_generator(self.train_set, steps_per_epoch=50,
                                 epochs=100, validation_data=self.validate_set, validation_steps=5)
        self.model.save(path)


trainer = Trainer()
trainer.train("train/model.h5")
