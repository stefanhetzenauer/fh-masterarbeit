import os
import pandas as pd
from datetime import datetime
from tqdm import tqdm

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

def load_data(path, label):
    files = os.listdir(path)
    full_df = pd.DataFrame()
    for file in tqdm(files):
        if file.endswith('_hist.csv'):
            df = pd.read_csv(path + r'/' + file, sep=';', encoding='utf-8')
            df['label'] = label
            full_df = full_df.append(df)
            
            del df
    return full_df

def create_training_csv(base_path, paths, filename):
    df_1 = load_data(base_path + paths[0], 0)
    df_2 = load_data(base_path + paths[1], 1)
    df_3 = load_data(base_path + paths[2], 2)
    
    full_df = df_1.append(df_2.append(df_3))
    
    full_df.to_csv(base_path + filename, sep=';', encoding='utf-8', index=False)

create_training_csv(BASE_PATH_DIFF, PATH_64_ASC, '64_asc-soa-v2.csv')
create_training_csv(BASE_PATH_DIFF, PATH_64_DESC, '64_desc-soa-v2.csv')

create_training_csv(BASE_PATH_DIFF, PATH_128_ASC, '128_asc-soa-v2.csv')
create_training_csv(BASE_PATH_DIFF, PATH_128_DESC, '128_desc-soa-v2.csv')

create_training_csv(BASE_PATH_SAME, PATH_64_SAME_95, '64_QF-95-soa-v2.csv')
create_training_csv(BASE_PATH_SAME, PATH_64_SAME_98, '64_QF-98-soa-v2.csv')
create_training_csv(BASE_PATH_SAME, PATH_64_SAME_100, '64_QF-100-soa-v2.csv')

create_training_csv(BASE_PATH_SAME, PATH_128_SAME_95, '128_QF-95-soa-v2.csv')
create_training_csv(BASE_PATH_SAME, PATH_128_SAME_98, '128_QF-98-soa-v2.csv')
create_training_csv(BASE_PATH_SAME, PATH_128_SAME_100, '128_QF-100-soa-v2.csv')
