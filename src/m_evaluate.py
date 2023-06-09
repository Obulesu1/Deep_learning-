import numpy as np
from keras_preprocessing.image import ImageDataGenerator
from keras.layers import Dense,Input,Flatten
from keras.models import Model
from glob import glob
import os
import argparse
from get_data import get_data
import matplotlib.pyplot as plt
from keras.applications.vgg19 import VGG19
import tensorflow
import pandas as pd
from sklearn.metrics import confusion_matrix, classification_report
import seaborn as sns
import tensorflow
from keras.models import load_model


def m_evaluate(config_file):
    config=get_data(config_file)
    batch =config["img_augment"]["batch_size"]
    class_mode = config["img_augment"]["class_mode"]
    te_set=config["model"]["test_path"]
    model = load_model('models/trained.h5')

    test_gen = ImageDataGenerator(rescale=1./255)

    test_set = test_gen.flow_from_directory(te_set, target_size=(255,255),batch_size=batch,class_mode=class_mode)

    label_map=(test_set.class_indices)
    print(label_map)

    Y_pred = model.predict(test_set,len(test_set))
    y_pred = np.argmax(Y_pred, axis=1)
    print("Confusion Matrix")

    sns.heatmap(confusion_matrix(test_set.classes,y_pred),annot=True)

    plt.xlabel('Actual values, 0:glioma_tumor, 1:meningioma_tumor, 2:no_tumor,3:pituitary_tumor')
    plt.ylabel('Predicted Values, 0:glioma_tumor, 1:meningioma_tumor, 2:no_tumor,3:pituitary_tumor')
    plt.savefig('reports/Confusion_matrix')
    #plt.show()

    print("Classification Report")
    target_names = ['glioma_tumor','meningioma_tumor','no_tumor','pituitary_tumor']
    df = pd.DataFrame(classification_report(test_set.classes, y_pred, target_names=target_names,output_dict=True)).T
    df['support']=df.support.apply(int)
    df.style.background_gradient(cmap='viridis',subset=pd.IndexSlice['0':'9','f1-score'])
    df.to_csv('reports/classification_report')
    print('Classification Report and Confusion Matrix Report are saved in reports folder of Template')

if __name__ == '__main__':

    args_parser = argparse.ArgumentParser()
    args_parser.add_argument('--config',default='params.yaml')
    passed_args = args_parser.parse_args()
    m_evaluate(config_file=passed_args.config)
    