"""
Module: logic
Description: This module provides functions to extract and transform GPS coordinates from image files.

Dependencies:
- pprint
- PIL (Python Imaging Library)
- pillow_heif
- piexif

Usage:
1. Import the module: `import logic`
2. Use functions like `logic.get_x_coordinate(file)` and `logic.get_y_coordinate(file)` to extract GPS coordinates.

"""

from pprint import pprint
from PIL import Image
from pillow_heif import register_heif_opener
import piexif
import pprint

codec = 'ISO-8859-1'

def get_x_coordinate(file):
    """
    Extracts and returns the X-coordinate (longitude) from the given image file.

    Parameters:
    - file (str): Path to the image file.

    Returns:
    - float: The X-coordinate (longitude) in decimal degrees.
    """
    register_heif_opener()
    image = Image.open(file)

    exif_dict = piexif.load(image.info.get('exif'))
    pprint.pprint(exif_dict)
    gps_dict = exif_transform(exif_dict)

    print('HERE:', gps_dict['GPSLongitude'])

    x_value = (convert_to_decimal_degrees(gps_dict['GPSLongitude'], 
                                        gps_dict['GPSLongitudeRef']))
    
    return x_value

def get_y_coordinate(file):
    """
    Extracts and returns the Y-coordinate (latitude) from the given image file.

    Parameters:
    - file (str): Path to the image file.

    Returns:
    - float: The Y-coordinate (latitude) in decimal degrees.
    """
    register_heif_opener()
    image = Image.open(file)

    exif_dict = piexif.load(image.info.get('exif'))
    pprint.pprint(exif_dict)
    gps_dict = exif_transform(exif_dict)

    x_value = (convert_to_decimal_degrees(gps_dict['GPSLatitude'], 
                                        gps_dict['GPSLatitudeRef']))
    
    return x_value

def exif_transform(exif_dict):
    """
    Helper function for the coordinates functions; reformats the data to a readable python dictionary.

    Parameters:
    - exif_dict (dict): Exif dictionary containing GPS information.

    Returns:
    - dict: Transformed GPS dictionary.
    """
    gps_dict = {}

    gps_dict['GPS'] = {}
    for tag in exif_dict['GPS']:
        try:
            element = exif_dict['GPS'][tag].decode(codec)
        except:
            element = exif_dict['GPS'][tag]

        gps_dict[piexif.TAGS['GPS'][tag]["name"]] = element
    
    return gps_dict

def convert_to_decimal_degrees(coordinate_arr, direction):
    degrees = coordinate_arr[0][0]
    minutes = coordinate_arr[1][0]
    seconds = coordinate_arr[2][0]

    decimal = degrees + minutes/60 + seconds/360000

    if (direction == 'W' or direction == 'S'):
        decimal = -decimal

    return decimal