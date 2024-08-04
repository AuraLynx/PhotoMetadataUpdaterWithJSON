import piexif
from datetime import datetime
from PIL import Image
import json
import os
from pathlib import Path
from tqdm import tqdm
import shutil
import traceback


out_file = Path("output")
error_file = Path("error")

def format_date_taken(str_date: str):
    datetime_obj = datetime.strptime(str_date, '%Y/%m/%d %H:%M:%S %Z')
    datetime_str = datetime_obj.strftime('%Y:%m:%d %H:%M:%S')
    return datetime_str

def get_date_taken(json_file):
    try:
        with open(json_file) as f:
            data = json.load(f)
    except UnicodeDecodeError as e:
        with open(json_file, encoding='cp932') as f:
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

def copy_img(image_path: Path, json_path: Path) -> None:
    img_name = image_path.name
    json_name = json_path.name

    if image_path.exists():
        img_output_path = error_file / img_name
        shutil.copy2(image_path, img_output_path)

    if json_path.exists():
        json_output_path = error_file / json_name
        shutil.copy2(json_path, json_output_path)

def main():
    print("Start...")
    photo_dir = Path('data/')
    photos_gen = photo_dir.glob('**/*.jpg')
    for imagefile in tqdm(photos_gen):
        print("file is ", imagefile)
        json_file = imagefile.with_name(imagefile.name + ".json")
        output_path = out_file / imagefile.name
        error_path = error_file / imagefile.name

        if not output_path.exists():
            try:
                date_taken = get_date_taken(json_file)
                date_taken = format_date_taken(date_taken)
                set_exif_date(imagefile, date_taken)
            except Exception as e:
                traceback.print_exc()
                print("Error at ", imagefile)
                print(e)
                copy_img(imagefile, json_file)
        else:
            print("Skip: ", imagefile)
            continue


if __name__ == '__main__':
    main()
