# This script allows resizing of pictures and making text and image watermarks.

import argparse
import ConfigParser
import os
import sys

try:
    from PIL import Image, ImageDraw, ImageEnhance, ImageFont
except ImportError:
    exit("This script requires the PIL module.\nInstall it please.")


def resize_image(filename, width, height, outfolder):
    """
    Resizes the image to width x height resolution and saves the
    image to outfolder in JPEG format.
    :filename: path to the input image
    :width: desired width of output image, an integer number
    :height: desired height of output image, an integer number
    :outfolder: path to the folder for the output image saving
    """
    image = Image.open(filename)
    imageWidth, imageHeight = image.size

    if width is None and height is not None:
        imageWidth = (imageWidth * height) / imageHeight
        imageHeight = height
    elif width is not None and height is None:
        imageHeight = (imageHeight * width) / imageWidth
        imageWidth = width
    elif width is not None and height is not None:
        imageWidth = width
        imageHeight = height

    resizedImage = image.resize((int(imageWidth), int(imageHeight)))
    resizedImage.save(os.path.join(outfolder, filename),'JPEG')


def text_watermark(filename, text, outfolder, angle=25, opacity=0.25):
    """
    Adds a text watermark to the image.
    :filename: path to the input image
    :text: text of a watermark
    :outfolder: path to the folder for the output image saving
    :angle: angle of the watermark text, a float number
    :opacity: watermark opacity, a float number from 0 to 1
    """
    font = 'Verdana.ttf'
    img = Image.open(filename).convert('RGB')
    watermark = Image.new('RGBA', img.size, (0,0,0,0))
    size = 2

    if sys.platform == "linux" or sys.platform == "linux2":
        font = os.path.join("/usr/share/fonts/truetype/msttcorefonts", font)

    # return FreeTypeFont(filename, size, index, encoding)
    n_font = ImageFont.truetype(font, size)
    n_width, n_height = n_font.getsize(text)
    while n_width+n_height < watermark.size[0]:
        size += 2
        n_font = ImageFont.truetype(font, size)
        n_width, n_height = n_font.getsize(text)
    draw = ImageDraw.Draw(watermark, 'RGBA')
    draw.text(((watermark.size[0] - n_width) / 2,
              (watermark.size[1] - n_height) / 2),
              text, font=n_font)
    watermark = watermark.rotate(float(angle), Image.BICUBIC)
    alpha = watermark.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(float(opacity))
    watermark.putalpha(alpha)
    Image.composite(watermark, img, watermark).save(os.path.join(outfolder, \
                    filename), 'JPEG')


def image_watermark(filename, watermark, outfolder, opacity=0.25):
    """
    Adds a watermark image to the input picture.
    :filename: path to the input image
    :watermark: path to the watermark image
    :outfolder: path to the folder for the output image saving
    :opacity: watermark opacity, a float number from 0 to 1
    """
    watermark = Image.open(watermark)
    if watermark.mode != 'RGBA':
        watermark = watermark.convert('RGBA')
    alpha = watermark.split()[3]
    #reduce the brightness or the 'alpha' band
    alpha = ImageEnhance.Brightness(alpha).enhance(float(opacity))
    watermark.putalpha(alpha)
    image = Image.open(filename)
    if image.mode != 'RGBA':
        image = image.convert('RGBA')
    if watermark.size[0] > image.size[0] or watermark.size[1] > image.size[1]:
        watermark = watermark.resize(image.size[0],image.size[1])
    layer = Image.new('RGBA', image.size, (0,0,0,0))
    position = (image.size[0]-watermark.size[0], image.size[1]-watermark.size[1])
    layer.paste(watermark, position)
    Image.composite(layer, image, layer).save(os.path.join(outfolder, filename))


def main():
    """Parses arguments from <config.cdf> using ConfigParser."""
    config = ConfigParser.ConfigParser()
    config.read("config.cfg")
    inputfolder = config.get('WATERMARKER', 'inputfolder')
    outfolder = config.get('WATERMARKER', 'outfolder')
    width = int(config.get('WATERMARKER', 'resolution').split(',')[0])
    height = int(config.get('WATERMARKER', 'resolution').split(',')[1])
    opacity = float(config.get('WATERMARKER', 'opacity'))
    angle = float(config.get('WATERMARKER', 'angle'))
    text = config.get('WATERMARKER', 'text')
    imagewatermark = config.get('WATERMARKER', 'imagewatermark')

    # change directory to inputfolder
    os.chdir(inputfolder)
    resolution = [width, height]
    if resolution:
        for filename in os.listdir(inputfolder):
            if filename.lower().endswith('.png') or filename.lower().\
                endswith('.jpg'):
                resize_image(filename, width, height, outfolder)

    # change directory to outfolder
    os.chdir(outfolder)
    if text is not None:
        for filename in os.listdir(outfolder):
            text_watermark(filename, text, outfolder, angle,opacity)

    if imagewatermark is not None:
        for filename in os.listdir(outfolder):
            image_watermark(filename, imagewatermark, outfolder, opacity)

if __name__ == '__main__':
    main()
