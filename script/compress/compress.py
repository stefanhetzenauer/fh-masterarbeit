from turbojpeg import TurboJPEG
from PIL import Image
import numpy as np
import os
from tqdm import tqdm
from datetime import datetime

LIB_PATH = r'*\turbojpeg.dll' # path to dll
PATH_TO_DATA = ''

# folder structure
# PATH_TO_DATA
# -> SIZExSIZE/TIF -- the raw images, the rest should be created automatically

def compress_image(jpeg, in_file_path, out_file_path, qf):
    with Image.open(in_file_path) as img:
        img_array = np.array(img)
        with open(out_file_path, 'wb') as out_img:
            out_img.write(jpeg.encode(img_array, quality=qf))

def compress(in_path, out_path, qf):
    jpeg = TurboJPEG(LIB_PATH)

    images = os.listdir(in_path)

    if not os.path.isdir(out_path):
        os.makedirs(out_path)
    
    for img in tqdm(images):
        img_name = img.split('.')[-2]
        compress_image(jpeg, f'{in_path}/{img}', f'{out_path}/{img_name}.JPG', qf)

def start_same_quality_factor_compression(sizes, qfs):
    for size in sizes:
        for qf in qfs:
            compress(f'{PATH_TO_DATA}/{size}x{size}/TIF', f'{PATH_TO_DATA}/{size}x{size}_QF-{qf}_1', qf)
            compress(f'{PATH_TO_DATA}/{size}x{size}_QF-{qf}_1', f'{PATH_TO_DATA}/{size}x{size}_QF-{qf}_2', qf)
            compress(f'{PATH_TO_DATA}/{size}x{size}_QF-{qf}_2', f'{PATH_TO_DATA}/{size}x{size}_QF-{qf}_3', qf)

def start_different_quality_factor_compression(sizes, qfs):
    for size in sizes:
        for qf1, qf2, qf3 in qfs:
            print(f'{datetime.now()}: Compressing size {size} with QF1: {qf1}!')
            compress(f'{PATH_TO_DATA}/{size}x{size}/TIF', f'{PATH_TO_DATA}/diff-{size}x{size}_QF1-{qf1}_1', qf1)
            print(f'{datetime.now()}: Compressing size {size} with QF1: {qf1} | QF2: {qf2}!')
            compress(f'{PATH_TO_DATA}/diff-{size}x{size}_QF1-{qf1}_1', f'.{PATH_TO_DATA}/diff-{size}x{size}_QF1-{qf1}-QF2-{qf2}_2', qf2)
            print(f'{datetime.now()}: Compressing size {size} with QF2: {qf2} | QF3: {qf3}!')
            compress(f'{PATH_TO_DATA}/diff-{size}x{size}_QF1-{qf1}-QF2-{qf2}_2', f'{PATH_TO_DATA}/diff-{size}x{size}_QF1-{qf1}-QF2-{qf2}_2_QF3-{qf3}', qf3)

start_same_quality_factor_compression(
    [64, 128],
    [95, 98, 100]
)

start_different_quality_factor_compression(
    [64, 128],
    [
        (95, 98, 100),
        (100, 98, 95)
    ]
)
