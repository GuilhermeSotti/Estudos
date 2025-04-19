from tensorflow.keras.preprocessing.image import ImageDataGenerator

def get_data_generators(train_dir, test_dir, img_size=(224, 224), batch_size=32, classes=None):

    train_datagen = ImageDataGenerator(
        rescale=1.0 / 255,
        rotation_range=20,
        width_shift_range=0.1,
        height_shift_range=0.1,
        shear_range=0.1,
        zoom_range=0.1,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    test_datagen = ImageDataGenerator(rescale=1.0 / 255)

    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=img_size,
        batch_size=batch_size,
        classes=classes,
        class_mode='categorical'
    )

    test_generator = test_datagen.flow_from_directory(
        test_dir,
        target_size=img_size,
        batch_size=batch_size,
        classes=classes,
        class_mode='categorical',
        shuffle=False
    )

    return train_generator, test_generator

def get_test_generator(test_dir, img_size=(224, 224), batch_size=32, classes=None):

    test_datagen = ImageDataGenerator(rescale=1.0 / 255)
    test_generator = test_datagen.flow_from_directory(
        test_dir,
        target_size=img_size,
        batch_size=batch_size,
        classes=classes,
        class_mode='categorical',
        shuffle=False
    )
    return test_generator
