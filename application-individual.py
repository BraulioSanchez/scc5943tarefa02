from GetData import GetData
from DataLoader import DataLoader
from PreProcessing import PreProcessing
from Model import Model

import os
import json
import numpy as np
import pandas as pd

if __name__ == "__main__":
    configs = json.load(open('config.json', 'r'))

    # download and process AMZN dataset
    GetData(configs['data']['symbol'],
                        configs['data']['start'],
                        configs['data']['end'],
                        configs).get_stock_data()
    dataloader = DataLoader(os.path.join(configs['data']['save_dir'], configs['data']['symbol'] + '.csv'),
                        configs['data']['train_test_split'],
                        configs['data']['columns'])

    preprocessing = PreProcessing()
    preprocessing.denoise(dataloader.data, configs)

    all_data = {configs['data']['column'][0]: preprocessing.denoised}

    # save all data preprocessed
    dataframe = pd.DataFrame(all_data)
    filename = os.path.join(configs['preprocessing']['save_dir'], configs['preprocessing']['filename'])
    dataframe.to_csv(filename, index=False)

    dataloader = DataLoader(filename,
                            configs['data']['train_test_split'],
                            configs['data']['columns'])

    # get train data
    X_train, y_train = dataloader.get_train_data(configs['data']['sequence_length'])
    print(X_train.shape, y_train.shape)

    model = Model()
    # build model
    model.build(configs)
    # training model
    model.train(X_train,
                y_train,
                epochs=configs['training']['epochs'],
                batch_size=configs['training']['batch_size'],
                save_dir=configs['model']['save_dir'])

    '''close = data_amzn.stock_data.Close
    preprocess = PreProcessing()
    preprocess.denoise(close)
    preprocess.to_csv()

    import matplotlib.pyplot as plt
    plt.plot(preprocess.preprocessed.scaled, color='red')
    plt.plot(preprocess.preprocessed.denoised, color='blue')
    plt.legend(['Scaled prices', 'Denoised prices'])
    plt.grid(True)
    plt.show()'''