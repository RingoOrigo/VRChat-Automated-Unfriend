import os, sys, pickle
from http.cookiejar import Cookie

class FileUtils:
    
    @staticmethod
    def resource_path (rel_path):
        """Get the absolute path to a resource"""
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, rel_path)
    
class CookieUtils:
    
    @staticmethod
    def store_cookies (cookies, file_name):
        """Locally store a user's cookie data for a smoother login process later."""
        with open(FileUtils.resource_path(file_name), "wb") as f:
            cookie_list = [c for c in cookies]
            pickle.dump(cookie_list, f)

    @staticmethod
    def load_cookies (file_name):
        """Retrieve locally stored cookies for use in the login process. Returns None if no cookies are found."""
        
        file = FileUtils.resource_path(file_name)
        
        if not os.path.exists(file):
            return None
        
        with open(file, 'rb') as f:
            cookies = pickle.load(f)

        return cookies

