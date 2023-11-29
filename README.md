### **- REMARK -**
Change branch to "feature" first
```bash
git checkout feature
```

# Image Proccesing Manga to Translator

Welcome to Manga to Translator, a Python-based project focusing on image processing for manga translation. This project aims to automate the translation of text within manga images

## Overview

Manga to Translator utilizes image processing techniques to identify text boxes within manga images, translates the text using Google Translate Library, and overlays the translated text onto the original image. The result is a web-based application where users can upload manga images, have the text translated, and view the translated manga.

## Workflow

1. **Open the Web Application:**
   - Users navigate to the web application.

2. **Upload Manga Image:**
   - Users upload a manga image to the system.

3. **Text Box Detection:**
   - The system uses YOLOv7 and YOLOv5 to detect text boxes within the manga image.

4. **Translation:**
   - The text within detected boxes is translated using the Google Translate Library.

5. **Overlay Translated Text:**
   - The translated text is overlaid onto the original manga image.

6. **Display on the Webpage:**
   - The translated manga is displayed on the webpage for users to view.

## Technology Stack

- **Python:**
  - The primary programming language for image processing and translation.

- **YOLOv7 and YOLOv5:**
  - Used for text box detection in manga images.

- **Google Translate Library:**
  - Utilized for translating text within the detected boxes.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Mini-Mark/ImageProccesing-Manga-to-translator.git
   cd ImageProccesing-Manga-to-translator/Webiste
2. **Open Website:**
   open file index.html
