import piexif
from datetime import datetime
from PIL import Image
import json
import os
from pathlib import Path


out_file = Path("output")

def format_date_taken(str_date: str):
    datetime_obj = datetime.strptime(str_date, '%Y/%m/%d %H:%M:%S %Z')
    datetime_str = datetime_obj.strftime('%Y:%m:%d %H:%M:%S')
    return datetime_str

def get_date_taken(json_file):
    with open(json_file) as f:
        data = json.load(f)
    return data.get('creationTime', {}).get('formatted', None)
    
def set_exif_date(image_path: Path, date_taken):
    exif_dict = piexif.load(str(image_path))
    exif_dict['Exif'][piexif.ExifIFD.DateTimeDigitized] = date_taken
    exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = date_taken
    exif_bytes = piexif.dump(exif_dict)

    im = Image.open(image_path)
    img_name = image_path.name
    output_path = out_file / img_name
    im.save(output_path, exif=exif_bytes)

def main():
    photo_dir = Path('\\192.168.11.13\TunaCatFolder\Helpme_Python\Takeout\Google フォト\Photos from 1998')
    photos = list(photo_dir.glob('**/*.jpg'))
    for imagefile in photos:
        print("total files are ", len(photos))
        print("file is ", imagefile)
        json_file = imagefile.with_name(imagefile.name + ".json")

        date_taken = get_date_taken(json_file)
        date_taken = format_date_taken(date_taken)
        set_exif_date(imagefile, date_taken)


if __name__ == '__main__':
    main()