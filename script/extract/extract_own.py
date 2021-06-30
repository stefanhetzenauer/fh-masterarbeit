import numpy as np
import pandas as pd
import os
import random
from datetime import datetime
from tqdm import tqdm

from jpeg2dct.numpy import load, loads


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
        # need to be set, tuple of coordinates
    ]
    valid_c = [
        # neet to be set, tuple of coordinates
    ]
    
    dct_y, dct_cb, dct_cr = extract_dct(file, raw_path)
    for x in range(0, 8):
        for y in range(0, 8):
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
            _hist_y, _ = create_histogram(
                extract_subband(x, y, dct_y),
                number_of_bins(x + 1, y + 1, True)
            )
            hist_y.append(_hist_y.tolist())
    result = flatten_list(hist_y) + flatten_list(hist_cb) + flatten_list(hist_cr)
    return pd.DataFrame(result).T

def save_data(df, out_path):
    df.to_csv(out_path, sep=';', encoding='utf-8', index=False)

def extract(img_dir, amount=5000):
    images = os.listdir(img_dir)
    print(f'{datetime.now()}: Extracting {img_dir}...')
    i = 0
    data = pd.DataFrame()
    for img in tqdm(images):
        i = i + 1
        if i > amount:
            break
        df = create_dct_data(img_dir + r'/' + img, img)
        data = data.append(df)
    return data

def create_dataset(paths, file_name):
    data = pd.DataFrame()
    for (path, label) in paths:
        df = extract(path)
        df['label'] = label
        data = data.append(df)
    save_data(data, file_name)

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

DATASET_NAME = ''

def create_same_datasets():
    print('1/6')
    create_dataset(
        [
            (BASE_PATH_SAME + PATH_64_SAME_95[0], 0),
            (BASE_PATH_SAME + PATH_64_SAME_95[1], 1),
            (BASE_PATH_SAME + PATH_64_SAME_95[2], 2)
        ],
        f'64_QF95-{DATASET_NAME}.csv'
    )

    print('2/6')
    create_dataset(
        [
            (BASE_PATH_SAME + PATH_64_SAME_98[0], 0),
            (BASE_PATH_SAME + PATH_64_SAME_98[1], 1),
            (BASE_PATH_SAME + PATH_64_SAME_98[2], 2)
        ],
        f'64_QF98-{DATASET_NAME}.csv'
    )

    print('3/6')
    create_dataset(
        [
            (BASE_PATH_SAME + PATH_64_SAME_100[0], 0),
            (BASE_PATH_SAME + PATH_64_SAME_100[1], 1),
            (BASE_PATH_SAME + PATH_64_SAME_100[2], 2)
        ],
        f'64_QF100-{DATASET_NAME}.csv'
    )

    print('4/6')
    create_dataset(
        [
            (BASE_PATH_SAME + PATH_128_SAME_95[0], 0),
            (BASE_PATH_SAME + PATH_128_SAME_95[1], 1),
            (BASE_PATH_SAME + PATH_128_SAME_95[2], 2)
        ],
        f'128_QF95-{DATASET_NAME}.csv'
    )

    print('5/6')
    create_dataset(
        [
            (BASE_PATH_SAME + PATH_128_SAME_98[0], 0),
            (BASE_PATH_SAME + PATH_128_SAME_98[1], 1),
            (BASE_PATH_SAME + PATH_128_SAME_98[2], 2)
        ],
        f'128_QF98-{DATASET_NAME}.csv'
    )

    print('6/6')
    create_dataset(
        [
            (BASE_PATH_SAME + PATH_128_SAME_100[0], 0),
            (BASE_PATH_SAME + PATH_128_SAME_100[1], 1),
            (BASE_PATH_SAME + PATH_128_SAME_100[2], 2)
        ],
        f'128_QF100-{DATASET_NAME}.csv'
    )

def create_diff_datasets():
    print('1/4')
    create_dataset(
        [
            (BASE_PATH_DIFF + PATH_64_ASC[0], 0),
            (BASE_PATH_DIFF + PATH_64_ASC[1], 1),
            (BASE_PATH_DIFF + PATH_64_ASC[2], 2)
        ],
        f'64_asc-{DATASET_NAME}.csv'
    )

    print('2/4')
    create_dataset(
        [
            (BASE_PATH_DIFF + PATH_64_DESC[0], 0),
            (BASE_PATH_DIFF + PATH_64_DESC[1], 1),
            (BASE_PATH_DIFF + PATH_64_DESC[2], 2)
        ],
        f'64_desc-{DATASET_NAME}.csv'
    )

    print('3/4')
    create_dataset(
        [
            (BASE_PATH_DIFF + PATH_128_ASC[0], 0),
            (BASE_PATH_DIFF + PATH_128_ASC[1], 1),
            (BASE_PATH_DIFF + PATH_128_ASC[2], 2)
        ],
        f'128_asc-{DATASET_NAME}.csv'
    )

    print('4/4')
    create_dataset(
        [
            (BASE_PATH_DIFF + PATH_128_DESC[0], 0),
            (BASE_PATH_DIFF + PATH_128_DESC[1], 1),
            (BASE_PATH_DIFF + PATH_128_DESC[2], 2)
        ],
        f'128_desc-{DATASET_NAME}.csv'
    )

create_same_datasets()
create_diff_datasets()