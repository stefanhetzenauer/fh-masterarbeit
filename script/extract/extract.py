from jpeg2dct.numpy import load, loads
import json
import os
from tqdm import tqdm
import numpy as np
import pandas as pd
from datetime import datetime

COMPRESSED_DIR = r''
COMPRESSED_DIFFERENT_DIR = r''
DCT_DIR = r''
DCT_DIFFERENT_DIR = r''

def extract(amount=5000):
    # make sure that directory exists
    if not os.path.isdir(DCT_DIFFERENT_DIR):
        os.makedirs(DCT_DIFFERENT_DIR)
    
    directories = os.listdir(COMPRESSED_DIFFERENT_DIR)
    print(directories)

    for directory in tqdm(directories):
        if not os.path.isdir(DCT_DIFFERENT_DIR + directory):
            os.makedirs(DCT_DIFFERENT_DIR + directory)
        images = os.listdir(COMPRESSED_DIFFERENT_DIR + directory)
        print(f'{datetime.now()}: Extracting {directory}...')
        i = 0
        for img in tqdm(images):
            i = i + 1
            if i > amount:
                break
            filename = img.split('.')[0]
            extract_dct(COMPRESSED_DIFFERENT_DIR + directory + r'/' + img, DCT_DIFFERENT_DIR + directory + r'/' + filename, directory.split('_')[-1])

def extract_dct(jpeg_file, out_path, true_label):
    with open(jpeg_file, 'rb') as src:
        buffer = src.read()
    dct_y, dct_cb, dct_cr = loads(buffer)
    try:
        df = create_histogram_dataframe(dct_y, dct_cb, dct_cr, true_label)
        df.to_csv(out_path + '_hist.csv', sep=';', encoding='utf-8', index=False)
    except Exception as e:
        print(e)

    

def save_numpy_file(out_path, data):
    pd.DataFrame(data.flatten()).to_csv(out_path, sep=';', encoding='utf-8', index=False)

def create_histogram(data):
    data = data.flatten().astype('float64')
    ptp = np.ptp(data)
    if ptp == 0:
        ptp = 1
    data_norm = 2. * (data - np.min(data)) / ptp - 1
    hist, bins = np.histogram(data_norm, bins=99)
    return hist, bins

def create_histogram_dataframe(dct_y, dct_cb, dct_cr, true_label):
    hist_y, _ = create_histogram(dct_y)
    hist_cb, _ = create_histogram(dct_cb)
    hist_cr, _ = create_histogram(dct_cr)
    
    true_label = list([true_label])
    df_y = pd.DataFrame(hist_y).T
    df_y.columns = ['y_' + str(i) for i in range(len(hist_y))]

    df_cb = pd.DataFrame(hist_cb).T
    df_cb.columns = ['cb_' + str(i) for i in range(len(hist_cb))]

    df_cr = pd.DataFrame(hist_cr).T
    df_cr.columns = ['cr_' + str(i) for i in range(len(hist_cr))]

    label = pd.DataFrame(true_label, columns=['label'])
    
    return pd.concat([df_y, df_cb, df_cr, label], 1)

extract()