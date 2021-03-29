from typing import List, Dict, Any
import URL
from pathlib import Path
from PIL import Image, ImageFont, ImageDraw
import io

def create_image(image_dict: Dict[str, Any], name="", folder="") -> None:
    final_name = name if name != "" else image_dict['name']

    path = create_image_path(name=final_name, extension=image_dict['ext'], folder=folder)
    if folder != "":
        Path(folder).mkdir(parents=True, exist_ok=True)
    
    write_image(path=path, data=image_dict['file'])

    print(f"Image Created for {image_dict['name']}")

# TODO: Implement Names functionality
def create_images(image_dicts: List[Dict[str, Any]], folder="") -> None:
    for image_dict in image_dicts:
        create_image(image_dict=image_dict, folder=folder)

def write_image(path: str, data) -> None:
    with Path(path).open(mode="wb") as file:
        file.write(data)

def create_image_path(name: str, extension: str, folder: str = "") -> str:
    if folder != "":
        return str(Path(folder).joinpath(name + extension))
    else:
        return name + extension

def mimetype_to_format(mimetype):
    types = {
        'image/png': "PNG",
        'image/jpeg': "JPEG"
    }
    assert types[mimetype], "Image format not supported!"

    return types[mimetype]

def create_barcode_labels_adapter(image_dicts, item_name="", width=750, height=350, font_path="assets/arial.ttf", bold_font_path="assets/arialbd.ttf"):
    for image_dict in image_dicts:
        image_dict['file'] = create_barcode_label(
            image_dict['file'], title=item_name, barcode_label=image_dict['name'],
            width=width, height=height, font_path=font_path, bold_font_path=bold_font_path,
            format=mimetype_to_format(image_dict['mimetype'])
            )
    return image_dicts

# TODO: Change Input Resolution, Add Scaling?
def create_barcode_label(barcode, title="", barcode_label="", width=750, height=350, font_path="assets/arial.ttf", bold_font_path="assets/arialbd.ttf", format="PNG"):
    white = (255, 255, 255)
    black = (0, 0, 0)

    barcode_image = Image.open(io.BytesIO(barcode))
    barcode_width, barcode_height = barcode_image.size

    gap_height = (height - barcode_height) / 2
    
    canvas = Image.new('RGB', (width, height), color=white)

    # Barcode
    barcode_paste_width = int(width / 2 - barcode_width / 2)
    barcode_paste_height = int(height / 2 - barcode_height / 2)
    canvas.paste(barcode_image, (barcode_paste_width, barcode_paste_height))

    # Loading Fonts
    font = ImageFont.truetype(font_path, size=12)
    bold_font = ImageFont.truetype(bold_font_path, size=16)
    draw = ImageDraw.Draw(canvas)
    
    # Title
    title_width, title_height = bold_font.getsize(title)
    title_draw_width = int(width / 2 - title_width / 2)
    title_draw_height = int(gap_height - 2 * title_height)
    draw.text((title_draw_width, title_draw_height), title, font=bold_font, fill=black)

    # Barcode Text
    barcode_label_width, barcode_label_height = font.getsize(barcode_label)
    barcode_label_draw_width = int(width / 2 - barcode_label_width / 2)
    barcode_label_draw_height = int(gap_height + barcode_height + barcode_label_height)
    draw.text((barcode_label_draw_width, barcode_label_draw_height), barcode_label, font=font, fill=black)

    # Save to Bytes
    buffer = io.BytesIO()
    canvas.save(buffer, format=format)
    return buffer.getvalue()