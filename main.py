from PIL import ImageFont, ImageDraw
import PIL.Image
import numpy as np
import pytesseract
import cv2
import matplotlib.pyplot as plt
from googletrans import Translator, LANGUAGES
import shutil
from IPython.display import Image, display
import glob
import os
import re


def get_last_exp_folder(path="."):
    # List all folders in the directory
    all_folders = [f for f in os.listdir(
        path) if os.path.isdir(os.path.join(path, f))]

    # Filter out folders that match the pattern "exp<number>"
    exp_folders = [f for f in all_folders if re.match(r'^exp\d*$', f)]

    # Extract numbers from the folder names
    numbers = [int(re.search(r'\d+', f).group())
               if re.search(r'\d+', f) else 0 for f in exp_folders]

    # If numbers list is empty, return "exp"
    if not numbers:
        return "exp"

    # Find the maximum number
    max_number = max(numbers)

    # Construct the folder name with the maximum number
    last_exp_folder = f"exp{max_number}" if max_number != 0 else "exp"

    return last_exp_folder

# Program


def translate_text(text, target_language):

    if(not(text == "" or text == None)):
        translator = Translator()
        translation = translator.translate(text, dest=target_language)
        return translation.text
    else:
        return ""


def wrap_text(text, font, max_width):
    """
    Wrap text based on specified width.
    This will return a list of lines of text.
    """
    words = text.split(' ')
    lines = []
    while words:
        line = ''
        # Check if the next word fits within the width
        if font.getbbox(words[0])[2] <= max_width:
            # Wrap by words
            while words and font.getbbox(line + words[0])[2] <= max_width:
                line += (words.pop(0) + ' ')
        else:  # If the word is too long
            # Wrap by characters
            while words and font.getbbox(line + words[0][0])[2] <= max_width:
                line += words[0][0]
                words[0] = words[0][1:]
            if not words[0]:  # If the word has been fully processed, remove it
                words.pop(0)
        lines.append(line)
    return lines


def extract_text_from_image(image_path, pos):
    # Open the image
    img = PIL.Image.open(image_path)
    optimize_read_width, optimize_read_height = img.size

    # Scale the image
    img_optimize_resized = img.resize(
        (optimize_read_width*1, optimize_read_height*1))

    # Set the tesseract command path
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    # Use pytesseract to extract text and its bounding box
    data = pytesseract.image_to_data(
        img_optimize_resized, lang='jpn_vert+jpn+eng', output_type=pytesseract.Output.DICT)

    # Iterate over the detected words and print the text and bounding box

    image_show = cv2.imread(image_path, cv2.COLOR_BGR2RGB)

    min_x, min_y = float('inf'), float('inf')
    max_x, max_y = -float('inf'), -float('inf')

    if all(not item.strip() for item in data['text']) or not data['text']:
        return

    for i in range(len(data['text'])):
        if data['text'][i].strip() != '':

            padding = 3

            text = data['text'][i]
            text_data = {
                "top-left": (data['left'][i] - padding, data['top'][i] - padding),
                "bottom-right": (data['left'][i] + data['width'][i] + padding, data['top'][i] + data['height'][i] + padding)
            }
            # print("----------------------------")
            # print(f"Text: {text}")
            # print(
            #     f"Top-Left: {text_data['top-left']}")
            # print(
            #     f"Bottom-Right: {text_data['bottom-right']}")

            # Text
            textbox_padding = 25
            min_x = min(min_x, data['left'][i] - textbox_padding)
            min_y = min(min_y, data['top'][i] - textbox_padding)
            max_x = max(max_x, data['left'][i] +
                        data['width'][i] + textbox_padding)
            max_y = max(max_y, data['top'][i] +
                        data['height'][i] + textbox_padding)

            # Fill Box
            color = (255, 255, 255)
            thickness = -1
            cv2.rectangle(
                image_show, text_data["top-left"], text_data["bottom-right"], color, thickness)

            # Bounding Box
            color = (255, 0, 0)
            thickness = 2
            #Check Text  Detection
            # cv2.rectangle(
            #     image_show, text_data["top-left"], text_data["bottom-right"], color, thickness)

    top_left = (min_x, min_y)
    bottom_right = (max_x, max_y)
      #Check TextBox
#     cv2.rectangle(image_show, top_left, bottom_right, (0, 255, 0), 2)

    label = translate_text(" ".join(data['text']), "th")
    print("".join(data['text']))
    print(label)

    # Wrap text using PIL
    fontpath = "./result/WR Tish Kid.ttf"
    font = ImageFont.truetype(fontpath, 28)
    max_width = bottom_right[0] - top_left[0]
    lines = wrap_text(label, font, max_width)

    # Convert OpenCV image to PIL image
    img_pil = PIL.Image.fromarray(cv2.cvtColor(image_show, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)

    # Write each line inside the rectangle using PIL
    y0, dy = top_left[1] + 20, 35

    total_text_height = len(lines) * dy
    y0 = top_left[1] + (bottom_right[1] - top_left[1] - total_text_height) // 2
    for i, line in enumerate(lines):
        y = y0 + i * dy
        # Calculate x-coordinate to center the text horizontally
        text_width = font.getbbox(line)[2]
        x = top_left[0] + (bottom_right[0] - top_left[0] - text_width) // 2
        draw.text((x, y), line, font=font, fill=(0, 0, 0))

    image_show = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

    with open(f"./yolov5/runs/detect/{get_last_exp_folder('./yolov5/runs/detect/')}/labels/test-crop-detail.txt", "r") as file:
        lines = file.readlines()

    # Select the number
    selected_line = lines[pos - 1]  # -1 because list indexing starts from 0

    # Extract the coordinates

    pos_top_left = tuple(map(int, selected_line.split(
        "|")[0].split(":")[1].strip().strip("()").split(",")))
    pos_bottom_right = tuple(map(int, selected_line.split(
        "|")[1].split(":")[1].strip().strip("()").split(",")))

    # ./test/images/test.jpg
    result_image = cv2.imread(
        f'./result/result_{get_last_exp_folder("./yolov5/runs/detect/")}.jpg')

    x, y = pos_top_left[0]-7, pos_top_left[1]-10

    if x < 0:
        x = 0
    if y < 0:
        y = 0

    h, w, _ = image_show.shape
    result_image[y:y+h, x:x+w] = image_show

    cv2.imwrite(
        f'./result/result_{get_last_exp_folder("./yolov5/runs/detect/")}.jpg', result_image)

# Get input from the user


def run():

    file_src = f'./yolov5/runs/detect/{get_last_exp_folder("./yolov5/runs/detect/")}/'
    shutil.copy('./upload_model_1/test.jpg',
                f'./result/result_{get_last_exp_folder("./yolov5/runs/detect/")}.jpg')

    print("Translate")
    pos = 1
    for imageName in glob.glob(f'{file_src}crops/text_bubble/*.jpg'):  # assuming JPG
        print(imageName)
        extract_text_from_image(imageName, int(imageName.replace(file_src, "").replace(
            'crops/text_bubble\\', "").replace("test", "").replace(".jpg", "")))
        pos += 1

    return f'./result/result_{get_last_exp_folder("./yolov5/runs/detect/")}.jpg'

# extract_text_from_image('./yolov5/runs/detect/exp2/crops/text_bubble/test12.jpg',12)
    # if(not(result_text == "" or result_text == None)):
    #   translated_text = translate_text(result_text, "th")
    #   print("----------------------------")
    #   print(f"Result: {result_text}")
    #   print(f"Translate: {translated_text}")
    #   print(f"Src: {imageName}")
