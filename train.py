import os
import fire
from datetime import datetime
from util import makepath

class Trainer(object):
    def __init__(self, pretrained="n", path=os.path.join(os.getcwd(), "train"), block=3): 
        if pretrained == "y" or pretrained == "Y":
            self.pretrained = True
        elif pretrained == "n" or pretrained == "N":
            self.pretrained = False
        else:
            raise Exception
        
        self.path = path
        
        self._get_datalabel()
        self.block = block
    
    def _get_datalabel(self):
        self.labellist = list()
        for folder in os.listdir(self.path):
            fullpath = os.path.join(self.path, folder)
            if os.path.isdir(fullpath):
                self.labellist.append(folder)
    
    def new_model(self):
        from keras.models import Sequential
        from keras.layers import Conv2D
        from keras.layers import MaxPooling2D
        from keras.layers import Flatten
        from keras.layers import Dropout
        from keras.layers import Dense
        
        model = Sequential()
        start_chan = 32
        model.add(Conv2D(8, kernel_size=(3,3), 
            activation='relu',
            input_shape=(64, 64, 3),
            padding="same"))
        model.add(MaxPooling2D(pool_size=(2,2)))
        for i in range(self.block):
            chan = start_chan*(i+1)
            model.add(Conv2D(chan, (3, 3), activation='relu', padding="same"))
            model.add(Conv2D(chan, (3, 3), activation='relu', padding="same"))
            model.add(MaxPooling2D(pool_size=(2,2)))
            # model.add(Dropout(0.2))
        model.add(Flatten())
        model.add(Dense(128, activation='relu'))
        model.add(Dropout(0.5))
        model.add(Dense(len(self.labellist), activation='softmax'))
        model.compile(loss='categorical_crossentropy',
            optimizer='rmsprop',
            metrics=['accuracy'])

        model.summary()
        return model


    def _data_generator(self):
        from keras.preprocessing.image import ImageDataGenerator

        train_data = ImageDataGenerator(rotation_range=30,
            width_shift_range=0.2,
            height_shift_range=0.2,
            shear_range=0.2,
            zoom_range=0.2,
            vertical_flip=True,
            validation_split=0.2)

        train_generator = train_data.flow_from_directory(
            directory = self.path,
            target_size=(64,64)
        )
        return train_generator

    def train(self, epoch=10):
        if not self.pretrained:
            model = self.new_model()
            dataset = self._data_generator()
            result = model.fit_generator(
                dataset,
                epochs=epoch
            )
            makepath('./model')
            model.save(f"./model/{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.h5")


if __name__=='__main__':
    fire.Fire(Trainer)