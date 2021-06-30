import requests
import pandas as pd

# downloads the .TIF files from the RAISE dataset

RAISE_CSV_PATH = ''
PATH_TO_RAW_DATA = ''

def load_data(path, sep=',', encoding='utf-8'):
    df = pd.read_csv(path, sep=sep, encoding=encoding)
    return df

def download_image(filename, url):
    r = requests.get(url, allow_redirects=True)
    open(filename, 'wb').write(r.content)

def download(in_path, out_path):
    data = load_data(in_path)
    length = len(data)

    for i, img in data.iterrows():
        filename = fr'{out_path}/{img["File"]}.TIF'
        url = img['TIFF']

        print(f'File {i} of {length} | {filename} | {url}')

        download_image(filename, url)

download(RAISE_CSV_PATH, PATH_TO_RAW_DATA)
