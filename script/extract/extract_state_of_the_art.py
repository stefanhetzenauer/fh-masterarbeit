import numpy as np
import pandas as pd
import os
from datetime import datetime
from tqdm import tqdm

from jpeg2dct.numpy import load, loads

BASE_PATH_SAME = r''
BASE_PATH_DIFF = r''

PATH_64_ASC = ['64x64_QF1-95_1', '64x64_QF1-95-QF2-98_2', '64x64_QF1-95-QF2-98_2_QF3-100']
PATH_64_DESC = ['64x64_QF1-100_1', '64x64_QF1-100-QF2-98_2', '64x64_QF1-100-QF2-98_2_QF3-95']

PATH_128_ASC = ['128x128_QF1-95_1', '128x128_QF1-95-QF2-98_2', '128x128_QF1-95-QF2-98_2_QF3-100']
PATH_128_DESC = ['128x128_QF1-100_1', '128x128_QF1-100-QF2-98_2', '128x128_QF1-100-QF2-98_2_QF3-95']

PATH_64_SAME_95 = ['64x64_QF-95_1', '64x64_QF-95_2', '64x64_QF-95_3']
PATH_64_SAME_98 = ['64x64_QF-98_1', '64x64_QF-98_2', '64x64_QF-98_3']
PATH_64_SAME_100 = ['64x64_QF-100_1', '64x64_QF-100_2', '64x64_QF-100_3']

PATH_128_SAME_95 = ['128x128_QF-95_1', '128x128_QF-95_2', '128x128_QF-95_3']
PATH_128_SAME_98 = ['128x128_QF-98_1', '128x128_QF-98_2', '128x128_QF-98_3']
PATH_128_SAME_100 = ['128x128_QF-100_1', '128x128_QF-100_2', '128x128_QF-100_3']

def number_of_bins(x, y, lu=True):
    if lu:
        if x + y == 2:
            return 170
        if x + y == 3:
            return 160
        if x + y == 4:
            return 110
        if x + y == 5:
            return 90
        if x + y == 6:
            return 70
        if x + y == 7:
            return 50
        if x + y == 8:
            return 45
        if x + y == 9:
            return 25
    else:
        if x + y == 2:
            return 100
        if x + y == 3:
            return 50
        if x + y == 4:
            return 30
        if x + y == 5:
            return 20
        if x + y == 6:
            return 10
        if x + y == 7:
            return 10
        if x + y == 8:
            return 10
        if x + y == 9:
            return 10

def flatten_list(l):
    return [item for sublist in l for item in sublist]

def create_histogram(data, bins):
    ptp = np.ptp(data)
    if ptp == 0:
        ptp = 1
    data_norm = 2. * (data - np.min(data)) / ptp - 1
    hist, bins = np.histogram(data_norm, bins=bins)
    return hist, bins

def extract_subband(x, y, dct):
    subband = list()
    for bands in dct:
        subband.append(bands[x][y])
    return subband

def extract_dct(jpeg_file, raw_path):
    with open(jpeg_file, 'rb') as src:
        buffer = src.read()
    dct_y, dct_cb, dct_cr = loads(buffer)

    shape_y = (256, 8, 8)
    shape_c = (64, 8, 8)

    if raw_path.startswith('64x64'):
        shape_y = (64, 8, 8)
        shape_c = (16, 8, 8)
    
    return np.absolute(np.reshape(dct_y, shape_y)), np.absolute(np.reshape(dct_cb, shape_c)), np.absolute(np.reshape(dct_cr, shape_c))

def create_dct_data(file, raw_path):
    hist_y = list()
    hist_cb = list()
    hist_cr = list()
    
    valid_lu = [
        # need do be set, tuple of coordinates
    ]
    valid_c = [
        # need to be set, tuple of coordinates
    ]
    
    dct_y, dct_cb, dct_cr = extract_dct(file, raw_path)
    for x in range(0, 8):
        for y in range(0, 8):
            if (x, y) in valid_c:
                _hist_cb, _ = create_histogram(
                    extract_subband(x, y, dct_cb),
                    number_of_bins(x + 1, y + 1, False)
                )
                hist_cb.append(_hist_cb.tolist())
                
                _hist_cr, _ = create_histogram(
                    extract_subband(x, y, dct_cr),
                    number_of_bins(x + 1, y + 1, False)
                )
                hist_cr.append(_hist_cr.tolist())
            if (x, y) in valid_lu:
                _hist_y, _ = create_histogram(
                    extract_subband(x, y, dct_y),
                    number_of_bins(x + 1, y + 1, True)
                )
                hist_y.append(_hist_y.tolist())
    result = flatten_list(hist_y) + flatten_list(hist_cb) + flatten_list(hist_cr)
    return pd.DataFrame(result).T

def save_data(df, out_path):
    df.to_csv(out_path + '_hist.csv', sep=';', encoding='utf-8', index=False)

def extract(img_dir, dct_dir, amount=5000):
    # make sure that directory exists
    if not os.path.isdir(dct_dir):
        os.makedirs(dct_dir)
    
    directories = os.listdir(img_dir)
    print(directories)

    for directory in tqdm(directories):
        if not os.path.isdir(dct_dir + directory):
            os.makedirs(dct_dir + directory)
        images = os.listdir(img_dir + directory)
        print(f'{datetime.now()}: Extracting {directory}...')
        i = 0
        for img in tqdm(images):
            i = i + 1
            if i > amount:
                break
            filename = img.split('.')[0]
            df = create_dct_data(img_dir + directory + r'/' + img, img)
            save_data(df, dct_dir + directory + r'/' + filename)

COMPRESSED_DIR = r''
COMPRESSED_DIFFERENT_DIR = r''
DCT_DIR = r''
DCT_DIFFERENT_DIR = r''

extract(COMPRESSED_DIR, DCT_DIR)
extract(COMPRESSED_DIFFERENT_DIR, DCT_DIFFERENT_DIR)
