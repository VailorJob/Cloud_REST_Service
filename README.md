# REST-API Cloud Service in Flask
This is a REST-API server for storing binary data in the S3 cloud service that uses the Flask framework

Python Version Used: Python 3.8-3.10

### Installation:
1. Ensure the python version is 3.8-3.10. To check, run $`python -V`.
2. Clone the Github repo: $`git clone https://github.com/VailorJob/Cloud_REST_Service.git`
3. Move into the project directory $`cd Cloud_REST_Service`
4. Setup a virtual environment in the project folder using python: $`python -m venv venv`
5. Start the virtual environment. You should see (venv) in as part of the command prompt once it is started: `.\venv\Scripts\activate` 
6. NOTE: To stop the virtual environment at any time, run (venv) $`deactivate`
7. Install all the requirements, including flask. Be sure not to use sudo as this will install flask in the global environment instead of the virtual environment: (venv) $ `pip install -r requirements.txt`

### To Run:
1. Run flask! (venv) $`flask run`
2. Go to http://127.0.0.1:5000 in a browser

# API Documentation
**Sing Up**
-
    Sign up user
* **URL**
    
    `/api/sign_up`


* **Method:**

    `POST`


* **URL Params**

    None


* **Data Params**

   * **Required:**

        `login=[string]`
        `password=[string]`
        `access_key_id=[your_aws_access_key_id]`
        `secret_access_key=[your_aws_secret_access_key]`


* **Success Response:**
  * **Code:** `200` <br />
  *  **Content:** `{"status_code": 200, "message": "You have successfully logged in"}`


* **Error Response:**
  * **Code:** `200` <br />
  * **Content:** `{"access_or_secret_key": "Not correct"}`

**Sing In**
-
    Sing in user
* **URL**
    
    `/api/sign_in`


* **Method:**

    `POST`


* **URL Params**

    None


* **Data Params**

  * **Required:**

      `login=[string]`
      `password=[string]`


* **Success Response:**
  * **Code:** `200` <br />
  *  **Content:** `{"status_code": 200, "message": "You have successfully logged in"}`
    

* **Error Response:**
  * **Code:** `200` <br />
  *  **Content:** `{"access_or_secret_key": "Not valid anymore, you can register again"}`
    
  **or if you sign in as admin:**
  * **Code:** `200` <br />
  *  **Content:** `{"access_or_secret_key": "Not valid, you need change keys in config"}`

**Create, Show and Delete Files**
-
    Get, Update and Delete File
* **URL**
    
    `/api/file/:key`


* **Method:**

    `GET`
    `PUT`
    `DELETE`


* **URL Params**
    
   * **Required:**
    
        `key=[string]`


* **Data Params**
    
  * **For method `PUT`:**

      `binary`


* **Success Response:**
  * **For method `GET`:**
    * **Code:** 200 <br />
    * **Content:** `Body`
    
  * **For method `PUT`:**
      * **Code:** 200 <br />
      * **Content:** `{"status_code": 200, "message": "File '{key}' uploaded successfully"}`
    
  * **For method `DELETE`:**
      * **Code:** 200 <br />
      * **Content:** `{}`


* **Error Response:**
  * **For method `GET`:**
    * **Code:** 200 <br />
    * **Content:** `{"message": "Not Found", "status_code": 404}`
    
  * **For method `PUT`:**
      * **Code:** 200 <br />
      * **Content:** `{"status_code": 400, "message": "File not specified"}`
    
  * **For method `DELETE`:**
      * **Code:** 200 <br />
      * **Content:** `{}`