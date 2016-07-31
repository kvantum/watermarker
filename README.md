# watermarker
Image resizer and watermark maker.

usage: watermarker.py [-h] [-r RESOLUTION [RESOLUTION ...]] [-o OPACITY]
                      [-a ANGLE] [-t TEXT] [-i [IMAGEWATERMARK]]
                      [inputfolder] [outfolder]

Images resizing and adding a watermark.

positional arguments:
  inputfolder           A folder of pictures to process
  outfolder             A folder for saving processed pictures.

optional arguments:
  -h, --help            show this help message and exit
  -r RESOLUTION [RESOLUTION ...], --resolution RESOLUTION [RESOLUTION ...]
                        Resize the picture resolution to <width> <height>.
  -o OPACITY, --opacity OPACITY
                        Sets the opacity of the watermark to <opacity>. This
                        is a number between 0 and 1.
  -a ANGLE, --angle ANGLE
                        Sets the angle for the text watermark.
  -t TEXT, --text TEXT  Sets the <text> watermark to the image.
  -i [IMAGEWATERMARK], --imagewatermark [IMAGEWATERMARK]
                        Sets the <path> to the watermark image.

