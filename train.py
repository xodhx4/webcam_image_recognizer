"""Make CNN model with your dataset

Make your CNN model with your dataset.
This automatically load dataset from directory './train/'.
This model is multi class classification and each folder would be onde class with dir name.
And this automatically augument the dataset with shift, flip, etc.

USAGE :
    python train.py train [--pretrained y|n] [--path DATASET_PATH] [--block NUM_BLOCK]
        [--BN True|False] [--epoch NUM_EPOCH]

TODO :
    [] Load pretrained model
    [] Finetune pretrained model
"""
import os
import fire
from datetime import datetime
from util import makepath


class Trainer(object):
    def __init__(self, pretrained="n", path=os.path.join(os.getcwd(), "train"), block=3, BN=True):
        """Init option - pretrained, path, block

        Args:
            pretrained (str): Defaults to "n". Whether use pretrained model or not. 
            path (string): Defaults to os.path.join(os.getcwd(), "train"). Path of dataset. 
            block (int): Defaults to 3. Block of CNN, Block is made in 2 CNN layer.
            BN (Boolean) : Defaults to True. Whether use batchnormalization or not.
        """
        if pretrained == "y" or pretrained == "Y":
            self.pretrained = True
        elif pretrained == "n" or pretrained == "N":
            self.pretrained = False
        else:
            raise Exception

        self.path = path

        self._get_datalabel()
        self.block = block
        self.BN = BN

    def _get_datalabel(self):
        """Make label list from dataset
        """
        self.labellist = list()
        for folder in os.listdir(self.path):
            fullpath = os.path.join(self.path, folder)
            if os.path.isdir(fullpath):
                self.labellist.append(folder)

    def _save_label(self, model_name):
        """Save Label data for inference

        Args:
            model_name (string): Name of model. label data will be saved as "{model_name}.txt"
        """
        label = ",".join(self.labellist)
        with open(f"{model_name}.txt", "w") as f:
            f.write(label)

    def new_model(self):
        """Generate CNN model
        """
        from keras.models import Sequential
        from keras.layers import Conv2D
        from keras.layers import MaxPooling2D
        from keras.layers import Flatten
        from keras.layers import Dropout
        from keras.layers import Dense
        from keras.layers import BatchNormalization

        model = Sequential()
        start_chan = 16
        model.add(Conv2D(8, kernel_size=(3, 3),
                         activation='relu',
                         input_shape=(64, 64, 3),
                         padding="same"))

        for i in range(self.block):
            chan = start_chan*(i+1)
            model.add(Conv2D(chan, (3, 3), activation='relu', padding="same"))
            model.add(Conv2D(chan, (3, 3), activation='relu', padding="same"))
            if self.BN:
                model.add(BatchNormalization())
            # model.add(MaxPooling2D(pool_size=(2,2)))
            # model.add(Dropout(0.2))
        model.add(Conv2D(1, (1, 1), activation='relu', padding="same"))
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
        """Load image from dir, and make augemented dataset
        """
        from keras.preprocessing.image import ImageDataGenerator

        train_data = ImageDataGenerator(rotation_range=30,
                                        width_shift_range=0.2,
                                        height_shift_range=0.2,
                                        shear_range=0.2,
                                        zoom_range=0.2,
                                        vertical_flip=True,
                                        validation_split=0.2)

        train_generator = train_data.flow_from_directory(
            directory=self.path,
            target_size=(64, 64)
        )
        return train_generator

    def train(self, epoch=10):
        """Train model with early stop
            epoch (int, optional): Defaults to 10. Number of epochs
        """
        from keras.callbacks import ModelCheckpoint, EarlyStopping

        if not self.pretrained:
            model = self.new_model()
            dataset = self._data_generator()
            model_name = f"./model/{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.h5"

            checkpoint = ModelCheckpoint(filepath=model_name,
                                         monitor="val_loss", verbose=1, save_best_only=True)
            early_stop = EarlyStopping()

            makepath('./model')

            result = model.fit_generator(
                dataset,
                epochs=epoch,
                callbacks=[checkpoint, early_stop]
            )
            # model.save(model_name)
            self._save_label(model_name)


if __name__ == '__main__':
    fire.Fire(Trainer)
