from pprint import pprint
from PIL import Image
from pillow_heif import register_heif_opener
import piexif
import pprint

codec = 'ISO-8859-1'

def get_x_coordinate(file):
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
    register_heif_opener()
    image = Image.open(file)

    exif_dict = piexif.load(image.info.get('exif'))
    pprint.pprint(exif_dict)
    gps_dict = exif_transform(exif_dict)

    print('HERE:', gps_dict['GPSLatitude'])

    x_value = (convert_to_decimal_degrees(gps_dict['GPSLatitude'], 
                                        gps_dict['GPSLatitudeRef']))
    
    return x_value

def exif_transform(exif_dict):
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