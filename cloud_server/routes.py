import hashlib
import uuid

import boto3
import cryptocode as crypto
from flask import render_template, request, make_response

from cloud_server import app, db
from cloud_server.aws_cloud import AWSCloud
from cloud_server.models import Users

AWSCLOUD = AWSCloud()
AUTHORIZED = False


def auth_check(foo):
    def wrapper(*args, **kwargs):
        if AUTHORIZED:
            return foo(*args, *kwargs)
        else:
            return {"status_code": 401, "message": "Cloud Server. Unauthorised"}

    return wrapper


@app.route("/")
def index():
    return render_template("index.html", title="Main")


@app.route("/api/sing_up", methods=["POST"])
def sing_up():
    global AUTHORIZED
    if AUTHORIZED:
        return {"status_code": 200, "message": "Cloud Server. You already authorized"}

    errors = {"login": False, "password": False, "access_key_id": False, "secret_access_key": False}
    if request.method == "POST":
        try:
            if not request.values.get('login'):
                errors["login"] = True

            if not request.values.get('password'):
                errors["password"] = True

            if not request.values.get('access_key_id'):
                errors["access_key_id"] = True

            if not request.values.get('secret_access_key'):
                errors["secret_access_key"] = True

            if True not in errors.values():
                salt = uuid.uuid4().hex

                password = request.values['password']

                access_key_id = crypto.encrypt(request.values['ak_id'], password)
                secret_access_key = crypto.encrypt(request.values['sak'], password)

                password = hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt

                if Users.query.filter(Users.login == request.values['login']).first():
                    errors["login"] = "Login busy"

                boto3.setup_default_session(aws_access_key_id=request.values['ak_id'],
                                            aws_secret_access_key=request.values['sak'])

                res = AWSCLOUD.login(errors["login"])
                if res:
                    errors["access_or_secret_key"] = "Not correct"

                check_errors = {i: errors[i] for i in errors if errors[i]}
                if check_errors:
                    AWSCLOUD.logout()
                    return check_errors
                else:
                    u = Users(login=request.values['login'], password=password, access_key_id=access_key_id,
                              secret_access_key=secret_access_key)

                    db.session.add(u)
                    db.session.commit()

                    AUTHORIZED = True
                    return {"status_code": 200, "message": f"You have successfully logged in"}
            else:
                return {i: f"Value is empty" for i in errors if errors[i]}

        except Exception as e:
            print(e)
            db.session.rollback()


@app.route("/api/sing_in", methods=["POST"])
def sing_in():
    global AUTHORIZED
    if AUTHORIZED:
        return {"status_code": 200, "message": "Cloud Server. You already authorized"}

    errors = {"login": False, "password": False}
    if request.method == "POST":

        if not request.values.get('login'):
            errors["login"] = True

        if not request.values.get('password'):
            errors["password"] = True

        if True not in errors.values():
            login = request.values['login']
            password = request.values['password']

            user = Users.query.filter(Users.login == login).first()
            if user:
                db_pass = user.password
                salt = db_pass.split(":")[1]
                if db_pass == hashlib.sha256(salt.encode() + password.encode()).hexdigest() + ':' + salt:
                    access_key_id = crypto.decrypt(user.access_key_id, password)
                    secret_access_key = crypto.decrypt(user.secret_access_key, password)
                    boto3.setup_default_session(aws_access_key_id=access_key_id,
                                                aws_secret_access_key=secret_access_key)
                    res = AWSCLOUD.login(errors["login"])
                    if res:
                        AWSCLOUD.logout()
                        db.session.delete(user)
                        db.session.commit()
                        return {"access_or_secret_key": f"Not valid anymore, you can register again"}
                    else:
                        AUTHORIZED = True
                        return {"status_code": 200, "message": f"You have successfully logged in"}
                else:
                    return {"password": f"'{password}' is not correct"}
            else:
                return {"login": f"'{login}' is not found"}
        else:
            return {i: f"Value is empty" for i in errors if errors[i]}


@auth_check
@app.route('/api/files_keys', methods=['GET'])
def get_files_keys():
    return AWSCLOUD.get_files_keys()


@auth_check
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


@auth_check
@app.route("/api/logout", methods=["GET"])
def logout():
    global AUTHORIZED
    AWSCLOUD.logout()
    AUTHORIZED = False
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
