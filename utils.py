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

    # @staticmethod
    # def make_cookie (name, value):
    #     """Create a cookie to allow for a smoother login process later."""
    #     return Cookie(0, name, value, None, False, "api.vrchat.cloud", True, False, "/", False, False, 173106866300, False, None, None, {})
    
    @staticmethod
    def store_cookies (cookies, file_name):
        """Locally store a user's cookie data for a smoother login process later."""
        with open(file_name, "wb") as f:
            cookie_list = [c for c in cookies]
            pickle.dump(cookie_list, f)

    @staticmethod
    def load_cookies (file_name):
        """Retrieve locally stored cookies for use in the login process. Returns None if no cookies are found."""
        if not os.path.exists(file_name):
            return None
        
        with open(file_name, 'rb') as f:
            cookies = pickle.load(f)

        return cookies

