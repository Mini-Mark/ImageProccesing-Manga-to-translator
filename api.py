from flask import Flask, request, render_template, jsonify
from flask_cors import CORS  # เพิ่มการนำเข้านี้
import base64
import os
from yolov5 import detect
import main
from PIL import Image
import io
import subprocess

app = Flask(__name__)
CORS(app)  # เปิดใช้ Flask-CORS สำหรับแอป Flask ของคุณ


# สร้างโฟลเดอร์เพื่อเก็บไฟล์ที่อัปโหลด
UPLOAD_FOLDER_MODEL_1 = 'upload_model_1'
UPLOAD_FOLDER_MODEL_2 = 'upload_model_2'


def image_to_base64(image_path):
    # Open the image
    with Image.open(image_path) as image:
        # Convert the image to bytes
        buffered = io.BytesIO()
        # You can change "PNG" to other formats like "JPEG" if needed
        image.save(buffered, format="PNG")

        # Encode the bytes to base64 and return
        img_str = base64.b64encode(buffered.getvalue())
        return img_str.decode('utf-8')


if not os.path.exists(UPLOAD_FOLDER_MODEL_1):
    os.makedirs(UPLOAD_FOLDER_MODEL_1)

if not os.path.exists(UPLOAD_FOLDER_MODEL_2):
    os.makedirs(UPLOAD_FOLDER_MODEL_2)

app.config['UPLOAD_FOLDER_MODEL_1'] = UPLOAD_FOLDER_MODEL_1
app.config['UPLOAD_FOLDER_MODEL_2'] = UPLOAD_FOLDER_MODEL_2


@app.route("/uploadModel1", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # รับไฟล์ภาพจากฟอร์ม
        uploaded_image = request.files["image"]

        if uploaded_image:
            # อ่านข้อมูลภาพ
            image_data = uploaded_image.read()

            # แปลงข้อมูลภาพเป็น Base64
            image_base64 = base64.b64encode(image_data).decode("utf-8")

            # บันทึกไฟล์ลงในเครื่อง
            filename = os.path.join(
                app.config['UPLOAD_FOLDER_MODEL_1'], 'test.jpg')

            # ตรวจสอบว่ามีไฟล์ชื่อเดียวกันอยู่แล้วหรือไม่
            if os.path.exists(filename):
                os.remove(filename)  # ลบไฟล์เดิม

            with open(filename, 'wb') as f:
                f.write(base64.b64decode(image_base64))

            detect.run(weights="./yolov5/runs/train/yolov5s_results/weights/best.pt",
                       conf_thres=0.75,
                       source="./upload_model_1/test.jpg",
                       save_crop=True,
                       save_txt=True)

            result = main.run("yolov5","upload_model_1")

            # ส่งข้อมูลภาพไปยังเทมเพลต
            return jsonify({"result": image_to_base64(result[0]),"detect": image_to_base64(result[1])})
    return jsonify({"Error": "Error"})


@app.route("/uploadModel2", methods=["GET", "POST"])
def index2():
    if request.method == "POST":
        # รับไฟล์ภาพจากฟอร์ม
        uploaded_image = request.files["image"]

        if uploaded_image:
            # อ่านข้อมูลภาพ
            image_data = uploaded_image.read()

            # แปลงข้อมูลภาพเป็น Base64
            image_base64 = base64.b64encode(image_data).decode("utf-8")

            # บันทึกไฟล์ลงในเครื่อง
            filename = os.path.join(
                app.config['UPLOAD_FOLDER_MODEL_2'], 'test.jpg')

            # ตรวจสอบว่ามีไฟล์ชื่อเดียวกันอยู่แล้วหรือไม่
            if os.path.exists(filename):
                os.remove(filename)  # ลบไฟล์เดิม

            with open(filename, 'wb') as f:
                f.write(base64.b64decode(image_base64))

            command = "python ./yolov7/detect_and_crop.py --weights ./yolov7/runs/train/result_100epoch/best.pt --conf 0.25 --source ./upload_model_2 --save-txt --save-conf"
            completed_process = subprocess.run(command, shell=True)

            if completed_process.returncode == 0:
                print("done!")
                result = main.run("yolov7","upload_model_2")
            else:
                print("The subprocess encountered an error.")


            # ส่งข้อมูลภาพไปยังเทมเพลต
            return jsonify({"result": image_to_base64(result[0]),"detect": image_to_base64(result[1])})
    return jsonify({"Error": "Error"})


if __name__ == "__main__":
    app.run(debug=True)
