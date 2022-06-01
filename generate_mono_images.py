from img2monoHMSD import write_bin
from PIL import Image
import os

def convert_images(source, destination):
    for root, dirs, files in os.walk(source):
        for file in files:
            source_path = os.path.join(root, file)
            destination_path = source_path.replace(source, destination).replace(".png", ".mono")

            print(f'Converting {source_path} to {destination_path}')

            os.makedirs(os.path.dirname(destination_path), exist_ok=True)

            # Open image and convert to monochrome
            image = Image.open(source_path).convert('1')
            pixels = list(image.getdata())

            with open(destination_path, 'wb') as f:
                write_bin(f, pixels, image.width)

def generate():
    convert_images("spritepng", "images")

if __name__ == '__main__':
    generate()
