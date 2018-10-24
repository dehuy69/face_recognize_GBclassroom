from flask import Flask, request, jsonify, render_template, Markup
from flask_dropzone import Dropzone
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class
from werkzeug.utils import secure_filename
import numpy as np
import cv2
import os
from processes import recognize, info, update_member_to_csv
from face_recognition import load_image_file
# Initialize the Flask application
app = Flask(__name__)
# Dropzone settings
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(basedir, 'facePhotos')
app.config.update(
    UPLOADED_PATH=os.path.join(basedir, 'facePhotos'),
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_TYPE='image',
    DROPZONE_MAX_FILE_SIZE=3,
    DROPZONE_MAX_FILES=20,
    DROPZONE_IN_FORM=True,
    DROPZONE_UPLOAD_ON_CLICK=True,
    DROPZONE_UPLOAD_ACTION='addmember',  # URL or endpoint
    DROPZONE_UPLOAD_BTN_ID='submit',
)
dropzone = Dropzone(app)
# route http posts to this method
@app.route('/api/recognizeface', methods=['POST'])
def recognizeface():
    r = request
    # convert string of image data to uint8
    nparr = np.fromstring(r.data, np.uint8)
    # decode image
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    print ('server print: ', img.shape)
    name = recognize(img)
    return jsonify({'name':name})

@app.route('/test', methods=['POST', 'GET'])
def test():
    if request.method == 'POST':
        if 'pic' in request.files:
            file = request.files['pic']
            filename = secure_filename(file.filename)
            im_path = os.path.join(app.config['UPLOADED_PATH'], filename)
            file.save(im_path)
            im = load_image_file(im_path)
            print (im)
            name = recognize(im)
            print (name)
    return render_template('test.html', im_path = im_path, face_name = name)


@app.route('/', methods=['POST', 'GET'])
def listofpeople():
    if request.method == 'GET':
        return render_template('index.html', infoTable = Markup(info.to_html()))
        # return render_template('index.html', infoTable = )
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        print('file uploaded and form submit<br>title: %s<br> description: %s' % (title, description))
        for key, f in request.files.items():
            if key.startswith('file'):
                f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
    return render_template('index.html')

@app.route('/addmember', methods=['POST'])
def addmember():
    if request.method == 'POST':
        print (request.form)
        nickname = request.form.get('nickname')
        name = request.form.get('name')
        age = request.form.get('age')
        gender = request.form.get('gender')
        job = request.form.get('job')
        info = update_member_to_csv(nickname, name, age, gender, job)
        print (name,age,gender,job)
        # print ("ten: %s, tuoi: %s, gioi tinh: %s, job: %s") %(name,age,gender,job)
        for key, f in request.files.items():
            if key.startswith('file'):
                f.save(os.path.join(app.config['UPLOADED_PATH'], f.filename))
    return render_template('index.html')

# start flask app
server_ip = '192.168.1.182'
app.run(host=server_ip, port=8080, debug=True)