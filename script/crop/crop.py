import os
import numpy as np
from tqdm import tqdm
from PIL import Image

def get_random_crop(image, crop_height, crop_width):
    # function to randomly crop given image
    max_x = image.shape[1] - crop_width
    max_y = image.shape[0] - crop_height

    x = np.random.randint(0, max_x)
    y = np.random.randint(0, max_y)

    crop = image[y: y + crop_height, x: x + crop_width]
    return crop

def load_image(image_path):
    with Image.open(image_path) as open_img:
        img = np.array(open_img)
        return img

def save_image(img, save_path):
    img = Image.fromarray(img)
    img.save(save_path)

def crop(in_path, out_path, size, amount):
    images = os.listdir(in_path)
    
    length = len(images)

    for i in tqdm(range(1, amount + 1)):
        rnd_index = np.random.randint(0, length)

        img_path = images[rnd_index]

        try:
            img = load_image(f'{in_path}/{img_path}')
            img = get_random_crop(img, size, size)
            save_image(img, f'{out_path}/{size}x{size}_{i}_{img_path}')

            del img
        except Exception as e:
            print('Something failed', e)
