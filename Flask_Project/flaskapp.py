import os
import io
from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
# import our OCR function
from ocr_core import ocr_core
from google.cloud import vision
import urllib.request
from werkzeug.utils import secure_filename
from utils.aws_text import  get_text
import cv2
from textblob import TextBlob
import base64
from PIL import Image, ImageGrab
from io import BytesIO

# define a folder to store and later serve the images
UPLOAD_FOLDER = "/home/ubuntu/flaskapp/static"

# allow files of a specific type
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]= os.path.join(app.config['UPLOAD_FOLDER'], 'json/ocrerror-aec7be99b182.json')
client = vision.ImageAnnotatorClient()
# function to check the file extension
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# route and function to handle the home page
@app.route('/')
def home_page():
    return render_template('index.html')

# route and function to handle the upload page
@app.route('/upload', methods=['GET', 'POST'])
def upload_page():
    if request.method == 'POST':
        # check if there is a file in the request
        if 'file' not in request.files:
            return render_template('upload.html', msg='No file selected')
        file = request.files['file']
        # if no file is selected
        if file.filename == '':
            return render_template('upload.html', msg='No file selected')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # call the OCR function on it
            extracted_text = ocr_core(file)

            # extract the text and display it
            return render_template('upload.html',
                                   msg='Successfully processed',
                                   extracted_text=extracted_text,
                                   result='Simple Tesseract OCR',
                                   img_src='http://13.126.63.255/'+'static/' + file.filename)
    elif request.method == 'GET':
        return render_template('upload.html')

@app.route('/upload-vision', methods=['GET', 'POST'])
def uploadvision_page():
    if request.method == 'POST':
        # check if there is a file in the request
        if 'file' not in request.files:
            return render_template('upload.html', msg='No file selected')
        file = request.files['file']
        # if no file is selected
        if file.filename == '':
            return render_template('upload.html', msg='No file selected')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # call the OCR function on it
            with io.open(os.path.join(app.config['UPLOAD_FOLDER'], file.filename), 'rb') as image_file: # use file.filename
                content = image_file.read()

            image = vision.Image(content=content)
            response = client.document_text_detection(image=image)
            texts= response.text_annotations
            extracted_text= texts[0].description
            #for text in texts:
                #extracted_text=  extracted_text+' '+text.description


            # extract the text and display it
            return render_template('upload.html',
                                   msg='Successfully processed',
                                   extracted_text=extracted_text,
                                    result='Google Vision OCR',
                                   img_src='http://13.126.63.255/'+'static/' + file.filename)
    elif request.method == 'GET':
        return render_template('upload.html')


@app.route('/upload-aws', methods=['GET', 'POST'])
def uploadaws_page():
    if request.method == 'POST':
        # check if there is a file in the request
        if 'file' not in request.files:
            return render_template('upload.html', msg='No file selected')
        file = request.files['file']
        # if no file is selected
        if file.filename == '':
            return render_template('upload.html', msg='No file selected')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # call the OCR function on it
            #with io.open(os.path.join(app.config['UPLOAD_FOLDER'], file.filename), 'rb') as image_file: # use file.filename
                #content = image_file.read()
            response,filename,res_response,statement = get_text(filename)
            #for text in texts:
                #extracted_text=  extracted_text+' '+text.description


            # extract the text and display it
            return render_template('upload.html',
                                   msg='Successfully processed',
                                   extracted_text=res_response,
                                   result='AWS OCR',
                                   img_src='http://13.126.63.255/'+'static/result_' + filename)
    elif request.method == 'GET':
        return render_template('upload.html')

@app.route('/upload-opencv', methods=['GET', 'POST'])
def uploadcv_page():
    if request.method == 'POST':
        # check if there is a file in the request
        if 'file' not in request.files:
            return render_template('upload.html', msg='No file selected')
        file = request.files['file']
        # if no file is selected
        if file.filename == '':
            return render_template('upload.html', msg='No file selected')

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # call the OCR function on it
            img=cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # Inverted Images
            #inverted_image=cv2.bitwise_not(img)
            gray_image=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            thresh,im_bw=cv2.threshold(gray_image,200,230,cv2.THRESH_BINARY)

            cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], "gray_"+filename),im_bw)

            extracted_text = ocr_core(os.path.join(app.config['UPLOAD_FOLDER'], "gray_"+filename))
            def noise_removal(image):
                 #import numpy as np
                 #kernel = np.ones((1, 1), np.uint8)
                 #image = cv2.dilate(image, kernel, iterations=1)
                 #kernel = np.ones((1, 1), np.uint8)
                 #image = cv2.erode(image, kernel, iterations=1)
                 #image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
                 image = cv2.medianBlur(image, 3)
                 return (image)
            img = noise_removal(im_bw)
            cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], "noise_"+filename),img)

            extracted_text2 = ocr_core(os.path.join(app.config['UPLOAD_FOLDER'], "noise_"+filename))
            tb = TextBlob(extracted_text)
            extracted_text2 = tb.correct()
            # extract the text and display it
            return render_template('upload2.html',
                                   msg='Successfully processed',
                                   extracted_text=extracted_text,
                                   result='Tesseract using OpenCV',
                                   img_src='http://13.126.63.255/'+'static/' + "gray_"+filename,
                                   extracted_text2=extracted_text2,
                                   img_src2='http://13.126.63.255/'+'static/' + "noise_"+filename)
    elif request.method == 'GET':
        return render_template('upload.html')


@app.route('/API/upload-opencv', methods=['POST'])
def uploadcv_page_api():
        record = request.get_json()
        if record and "fileName" in record:
            fileName = record['fileName']
        else:
            return jsonify({'status': 200,'text':'no records fileName'})
        if record and "photo" in record:
            photo = record['photo']
        else:
            return jsonify({'status': 200,'text':'no records photo'})
        bytes_decoded = base64.b64decode(record['photo'])
        img = Image.open(BytesIO(bytes_decoded))
        out_jpg = img.convert("RGB")
        out_jpg.save(os.path.join(app.config['UPLOAD_FOLDER'], record['fileName']))
        if out_jpg and allowed_file(record['fileName']):
            # call the OCR function on it
            img=cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], record['fileName']))
            # Inverted Images
            #inverted_image=cv2.bitwise_not(img)
            gray_image=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            thresh,im_bw=cv2.threshold(gray_image,173,230,cv2.THRESH_BINARY)

            cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], "gray_"+record['fileName']),im_bw)

            extracted_text = ocr_core(os.path.join(app.config['UPLOAD_FOLDER'], "gray_"+record['fileName']))
            def noise_removal(image):
                 #import numpy as np
                 #kernel = np.ones((1, 1), np.uint8)
                 #image = cv2.dilate(image, kernel, iterations=1)
                 #kernel = np.ones((1, 1), np.uint8)
                 #image = cv2.erode(image, kernel, iterations=1)
                 #image = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)
                 image = cv2.medianBlur(image, 3)
                 return (image)
            img = noise_removal(im_bw)
            cv2.imwrite(os.path.join(app.config['UPLOAD_FOLDER'], "noise_"+record['fileName']),img)

            extracted_text2 = ocr_core(os.path.join(app.config['UPLOAD_FOLDER'], "noise_"+record['fileName']))
            tb = TextBlob(extracted_text)
            extracted_text2 = tb.correct()
            # extract the text and display it
            return jsonify({'status': 200,'text':extracted_text})

@app.route('/API/upload-aws', methods=['POST'])
def uploadawsapi_page():
            record = request.get_json()
            if record and "fileName" in record:
                    fileName = record['fileName']
            else:
                    return jsonify({'status': 200,'text':'no records fileName'})
            if record and "photo" in record:
                    photo = record['photo']
            else:
                    return jsonify({'status': 200,'text':'no records photo'})
            bytes_decoded = base64.b64decode(record['photo'])
            img = Image.open(BytesIO(bytes_decoded))
            out_jpg = img.convert("RGB")
            out_jpg.save(os.path.join(app.config['UPLOAD_FOLDER'], record['fileName']))
            # call the OCR function on it
            #with io.open(os.path.join(app.config['UPLOAD_FOLDER'], file.filename), 'rb') as image_file: # use file.filename
                #content = image_file.read()
            response,filename,res_response,statement = get_text(record['fileName'])
            #for text in texts:
                #extracted_text=  extracted_text+' '+text.description


            # extract the text and display it
            return jsonify({'status': 200,'text':res_response})

@app.route('/API/upload-vision', methods=['POST'])
def uploadvisionapi_page():
            record = request.get_json()
            if record and "fileName" in record:
                fileName = record['fileName']
            else:
                return jsonify({'status': 200,'text':'no records fileName'})
            if record and "photo" in record:
                photo = record['photo']
            else:
                return jsonify({'status': 200,'text':'no records photo'})
            bytes_decoded = base64.b64decode(record['photo'])
            img = Image.open(BytesIO(bytes_decoded))
            out_jpg = img.convert("RGB")
            out_jpg.save(os.path.join(app.config['UPLOAD_FOLDER'], record['fileName']))
            # call the OCR function on it
            with io.open(os.path.join(app.config['UPLOAD_FOLDER'],record['fileName']), 'rb') as image_file: # use file.filename
                content = image_file.read()

            image = vision.Image(content=content)
            response = client.text_detection(image=image)
            texts= response.text_annotations
            extracted_text= texts[0].description
            #for text in texts:
                #extracted_text=  extracted_text+' '+text.description


            # extract the text and display it
            return jsonify({'status': 200,'text':extracted_text})


if __name__ == '__main__':
    app.run()
