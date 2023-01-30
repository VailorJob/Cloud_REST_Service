import dropbox
from dropbox import DropboxOAuth2FlowNoRedirect
from werkzeug.utils import secure_filename
import os

APP_KEY = ""
APP_SECRET = ""

class DropBoxService:
    def __init__(self, APP_KEY, APP_SECRET):
        self.dropbox_folder_path = "/Binary"
        self.serv_folder_path = "bin/"
        self._auth_flow = DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET)
        self._authorize_url = _auth_flow.start()

    

