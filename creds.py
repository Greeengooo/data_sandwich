from config import CONFIG
import base64


class Credentials():
    def __init__(self):
        self.username = base64.b64decode(CONFIG['uid']).decode()
        self.password = base64.b64decode(CONFIG['pwd']).decode()
    
    def get_creds(self):
        return dict(
                host = CONFIG['host'],
                port = CONFIG['port'],
                uid = self.username,
                pwd = self.password,
                driver = CONFIG['driver'],      
                )
