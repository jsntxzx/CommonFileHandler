import os

from flask import Flask, request, render_template, jsonify
from flask import send_from_directory
from flask import url_for

UPLOAD_FOLDER = 'upload'
SECRET_KEY = 'M0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
ALLOWED_EXTENSION = ['jpg', 'gif', 'png']

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = SECRET_KEY


def get_file_size(filename):
    st = os.stat(os.path.join(UPLOAD_FOLDER, filename))
    return st.st_size


def list_files():
    ret = []
    for f in os.listdir(UPLOAD_FOLDER):
        filepath = os.path.join(UPLOAD_FOLDER, f)
        if os.path.isfile(filepath):
            ret.append(f)
    return ret


@app.route('/')
def main():
    return render_template('basic.html')


@app.route('/download/<path:filename>')
def download(filename):
    return send_from_directory(directory=UPLOAD_FOLDER, filename=filename)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        # we are expected to return a list of dicts with infos about the already available files:
        file_infos = []
        for file_name in list_files():
            file_url = url_for('download', filename=file_name)
            file_size = get_file_size(file_name)
            file_infos.append(dict(name=file_name,
                                   size=file_size,
                                   url=file_url))
        return jsonify(files=file_infos)

    if request.method == 'POST':
        # we are expected to save the uploaded file and return some infos about it:
        data_file = request.files.get('files[]')
        file_name = data_file.filename
        data_file.save(os.path.join(UPLOAD_FOLDER, file_name))

        file_size = get_file_size(file_name)
        file_url = url_for('download', filename=file_name)

        file_info = {
            "name" : file_name,
            "size" : file_size,
            "url"  : file_url,
            "minetype" :  data_file.content_type
        }
        return jsonify(files = [file_info])


if __name__ == '__main__':
    app.run()