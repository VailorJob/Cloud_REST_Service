import hashlib
import uuid

import boto3
import cryptocode as crypto
from flask import render_template, request, url_for, redirect, send_from_directory, make_response

from cloud_server import app, db
from cloud_server.aws_cloud import AWSCloud
from cloud_server.models import Users

AWSCLOUD = AWSCloud()


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

            if Users.query.filter(Users.login == request.form['login']).first():
                errors["login"] = True

            boto3.setup_default_session(aws_access_key_id=request.form['ak_id'],
                                        aws_secret_access_key=request.form['sak'])

            res = AWSCLOUD.login(errors["login"])
            if res:
                errors["access_key_id"] = True
                errors["secret_access_key"] = True

            if True in errors.values():
                return render_template("sing_up.html", title="Sing up", errors=errors)
            else:
                u = Users(login=request.form['login'], password=password, access_key_id=access_key_id,
                          secret_access_key=secret_access_key)

                db.session.add(u)
                db.session.commit()

            return redirect(url_for("index"))
            # return {"status_code": 200, "message": f"You have successfully logged in"}

        except Exception as e:
            print(e)
            db.session.rollback()

    return render_template("sing_up.html", title="Sing up", errors=errors)


@app.route("/sing_in", methods=["POST", "GET"])
def sing_in():
    errors = {"login": False, "password": False}
    if request.method == "POST":
        login = request.form['login']
        password = request.form['password']

        user = Users.query.filter(Users.login == login).first()
        if user:
            db_pass = user.password
            salt = db_pass.split(":")[1]
            if db_pass == hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt:
                access_key_id = crypto.encrypt(request.form['ak_id'], password)
                secret_access_key = crypto.encrypt(request.form['sak'], password)
                boto3.setup_default_session(aws_access_key_id=access_key_id,
                                            aws_secret_access_key=secret_access_key)
        else:
            errors["login"] = True

    return render_template("sing_in.html", title="Sing in", errors=errors)


@app.route("/api/all_users", methods=["GET"])
def users_dict():
    return [db_user() for db_user in Users.query.all()]


@app.route('/api/files_keys', methods=['GET'])
def get_files_keys():
    return AWSCLOUD.get_files_keys()


@app.route('/api/file/<path:key>', methods=['GET', 'PUT', 'DELETE'])
def get_file(key):
    if request.method == "GET":
        return AWSCLOUD.get_file(key)
    elif request.method == "PUT":
        file_data = request.get_data()
        if not file_data:
            return {"status_code": 400, "message": "File not specified"}
        else:
            res = AWSCLOUD.put_file(key, file_data)
            return res or {"status_code": 200, "message": f"File '{key}' uploaded successfully"}
    elif request.method == "DELETE":
        AWSCLOUD.delete_file(key)
        return {}


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
