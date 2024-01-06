from flask import Flask, jsonify, render_template, request, flash, redirect, url_for
import json
from json import JSONEncoder
import warnings
from werkzeug.utils import secure_filename
import os
from files.VEnc import VEnc
warnings.filterwarnings("ignore")
app = Flask (__name__)

UPLOAD_FOLDER = 'C:\\Users\\shris\\Downloads\\Video-Security-Application\\uploads'
ALLOWED_EXTENSIONS = {'mp4', 'avi', 'mov'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods = ['GET', 'POST'])
def home():
    return render_template('index.html', show=1, res=None)

@app.route('/upload', methods = ['GET','POST'])
def func():
    if request.method == 'POST':
        # try:
        #     url = request.form['url']
        #     if 'examples' in url:
        #         return render_template('index.html', res=1)
        # except:
        #     print()
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            print(filename)
            password = request.form.get("pass") 
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            s = VEnc(os.path.join(app.config['UPLOAD_FOLDER'], filename), mode="video")
            s.set_password(password)
            choice = request.form['mode']
            if(choice == "encrypt"):
                print(app.root_path, app.instance_path)
                s.encrypt("encryption.mp4")
                os.replace("tmp_encryption.mp4", "static/encryption.mp4")
                return render_template('index.html', res = "/static/encryption.mp4", show=None)
            else:
                s.decrypt("decryption.mp4")
                os.replace("tmp_decryption.mp4", "static/decryption.mp4")
                return render_template('index.html', res = "/static/decryption.mp4", show=None)
    return render_template('index.html', error="Error! Please Try Again")
if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.run(debug=False)