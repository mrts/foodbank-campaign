# coding: utf-8

import os

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL import ImageOps

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.join(BASE_DIR, 'campaigns', 'static', 'campaigns')

FONT_FILE = os.path.join(BASE_DIR, 'fonts', 'roboto-medium.ttf')
LOGO_FILE = os.path.join(BASE_DIR, 'img', 'toidupanga-logo.png')

def draw_text_on_logo(line1, line2, output_filename):
    '''
    >>> line1 = u'TOIDUKOGUMISPÄEVAD'
    >>> line2 = u'9.12 – 10.12'
    >>> output_filename = '../htdocs/static/generated/test.png'
    >>> draw_text_on_logo(line1, line2, output_filename)
    '''
    font = ImageFont.truetype(FONT_FILE, 10)
    logo = Image.open(LOGO_FILE)
    logo.thumbnail((120, 120))

    logo_height = logo.size[1]
    text_height = font.getsize(line1)[1]
    left_border = 3
    first_line_offset = 2
    line_gap = 3
    expand = text_height * 2 + line_gap * 2 + first_line_offset

    canvas = Image.new('RGBA', (logo.size[0], logo.size[1] + expand), 'white')
    canvas.paste(logo, (0, 0))

    draw = ImageDraw.Draw(canvas)

    first_line_offset = logo_height + first_line_offset
    draw.text((left_border, first_line_offset), line1, 'black', font=font)

    second_line_offset = first_line_offset + line_gap + text_height
    draw.text((left_border, second_line_offset), line2, 'black', font=font)

    canvas = ImageOps.expand(canvas, border=2, fill='white')

    _save_file(canvas, output_filename)

def _save_file(image, output_filename):
    try:
        image.save(output_filename)
    except IOError:
        output_dir = os.path.dirname(output_filename)
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)
            image.save(output_filename)
        else:
            raise

