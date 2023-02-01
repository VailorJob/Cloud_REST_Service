from cloud_server import app, db
from cloud_server.models import Users
from cloud_server.aws_cloud import AWSCloud, boto3
from flask import render_template, request, url_for, redirect, send_from_directory, make_response
import cryptocode as crypto
import uuid
import hashlib
from markupsafe import escape


@app.route("/")
def index():
    return render_template("index.html", title="Main")

@app.route("/sing_up", methods=["POST", "GET"])
def sing_up():
    errors = {"login": False, "password": False, "access_key_id": False, "secret_access_key": False}
    if request.method == "POST":
        try:
            if request.form['password'] != request.form['check_password']:
                errors["password"] = True

                salt = uuid.uuid4().hex

                password = request.form['password']

                access_key_id = crypto.encrypt(request.form['ak_id'], password)
                secret_access_key = crypto.encrypt(request.form['sak'], password)

                password = hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt

                u = Users(login=request.form['login'], password=password, access_key_id=access_key_id, secret_access_key=secret_access_key)

                db.session.add(u)
                db.session.commit()

                boto3.setup_default_session(aws_access_key_id=request.form['ak_id'], aws_secret_access_key=request.form['sak'])

                return render_template("sing_up.html", title="Welcome!", register_complete="True")

        except Exception as e:
            db.session.rollback()
            print(e)

            errors["login"] = True

    return render_template("sing_up.html", title="Sing up", errors=errors)

@app.route("/sing_in", methods=["POST", "GET"])
def sing_in():
    if request.method == "POST":
        user = get_user(request.form['username'])
        if user.check_password(request.form['password']):
            login_user(user)
            app.logger.info('%s logged in successfully', user.username)
            return redirect(url_for('index'))
        else:
            app.logger.info('%s failed to log in', user.username)
            abort(401)

    return render_template("sing_in.html", title="Sing in")

@app.route("/api/put", methods=['GET', 'POST'])
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

@app.route('/api/uploads/')
@app.route('/api/uploads/<path:name>')
def view_file(name=None):
    if name:
        print(os.listdir(os.path.join(PROJECT_FOLDER, app.config['UPLOAD_FOLDER'], name)))
    else:
        print(os.listdir(os.path.join(PROJECT_FOLDER, app.config['UPLOAD_FOLDER'])))

    return ""

@app.route('/api/get/<path:name>')
def get_file(name=None):
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