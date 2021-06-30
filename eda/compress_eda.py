from turbojpeg import TurboJPEG
from PIL import Image
import numpy as np
import os
from tqdm import tqdm
from datetime import datetime

LIB_PATH = r'turbojpeg.dll' # path to turbojpeg dll

def compress_image(jpeg, in_file_path, out_file_path, qf):
    """Compresses the given image with the given quality factor.

    Args:
        jpeg: The opened TurboJPEG object
        in_file_path (string): The path to the file that should be compressed
        out_file_path (string): The destination of the compressed file
        qf (int): The quality factor of the JPEG compression
    """    ''''''
    with Image.open(in_file_path) as img:
        img_array = np.array(img)
        with open(out_file_path, 'wb') as out_img:
            out_img.write(jpeg.encode(img_array, quality=qf))

def compress(in_path, out_path, qf):
    '''Method to compress images by given path into given path and given qualitfactor.

    Args:
        in_path (string): Path to a folder that consists of images
        out_path (string): Path to folder where compressed images should be saved into
        qf (int): Quality factor of the compression
    '''
    jpeg = TurboJPEG(LIB_PATH)

    images = os.listdir(in_path)

    if not os.path.isdir(out_path):
        os.makedirs(out_path)
    
    for img in tqdm(images):
        img_name = img.split('.')[-2]
        compress_image(jpeg, f'{in_path}/{img}', f'{out_path}/{img_name}.JPG', qf)

