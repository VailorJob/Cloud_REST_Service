from flask import Flask, render_template, request, url_for, redirect, send_from_directory, make_response
from markupsafe import escape
import os

PROJECT_FOLDER = "cloud_server"
UPLOAD_FOLDER = "uploads"

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/")
def index():
    return render_template("index.html", title="Main")

@app.route("/sing_in", methods=["POST"])
def sing_in():
    user = get_user(request.form['username'])
    if user.check_password(request.form['password']):
        login_user(user)
        app.logger.info('%s logged in successfully', user.username)
        return redirect(url_for('index'))
    else:
        app.logger.info('%s failed to log in', user.username)
        abort(401)

@app.route("/upload", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files["file"]
        filename = secure_filename(file.filename)
        index = filename.index(".")
        name, extension = filename[:index], filename[index:]
        if info_extension(filename):
            path_filename = info_extension(filename) + "/" + filename
            full_path = os.path.join(PROJECT_FOLDER, app.config['UPLOAD_FOLDER'], path_filename)
            pref = 1
            while os.path.exists(full_path):
                path_filename = info_extension(filename) + "/" + name + "_" + str(pref) + extension
                full_path = os.path.join(PROJECT_FOLDER, app.config['UPLOAD_FOLDER'], path_filename)
                pref += 1
                    
            file.save(full_path)

            return redirect(url_for('download_file', name=path_filename))

    return render_template("upload.html", title="Download file")

@app.route('/uploads/')
@app.route('/uploads/<path:name>')
def view_file(name=None):
    if name:
        print(os.listdir(os.path.join(PROJECT_FOLDER, app.config['UPLOAD_FOLDER'], name)))
    else:
        print(os.listdir(os.path.join(PROJECT_FOLDER, app.config['UPLOAD_FOLDER'])))

    return ""

@app.route('/download/<path:name>')
def download_file(name=None):
    if name:
        return send_from_directory(app.config["UPLOAD_FOLDER"], name)
    else:
        print(os.listdir(os.path.join(PROJECT_FOLDER, app.config['UPLOAD_FOLDER'])))

@app.errorhandler(404)
def page_not_found(error):
    resp = make_response(render_template('page_not_found.html', title="Page Not Found"), 404)
    # Responses
    resp.headers["X-Something"] = "A Value"
    # Cookie
    resp.set_cookie("username", "the username")
    # get cookie
    username = request.cookies.get('username')
    return resp

