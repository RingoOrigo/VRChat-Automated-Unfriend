import os, sys, pickle, time, random
from vrchatapi.exceptions import ApiException

class APIUtils:
    """A helper class to implement an exponential delay to decrease the odds of being rate-limited."""
    limit_break = 1
    
    @staticmethod
    def make_delayed_request (request, *args, **kwargs):
        """Delay making a request by a set amount of time. Implement exponential backoff."""
        exp_backoff = 2 ** APIUtils.limit_break
        random_mod = random.uniform(0, 1)

        time.sleep(exp_backoff + random_mod)

        try: 
            result = request(*args, **kwargs)
            APIUtils.limit_break = 1
            return result
        
        except ApiException as e:
            if e.status == 429:
                APIUtils.limit_break += 1
                return APIUtils.make_delayed_request(request, *args, **kwargs)
            else:
                raise e

class FileUtils:
    
    @staticmethod
    def resource_path (rel_path):
        """Get the absolute path to a resource"""

        # As pyinstaller references directories differently, first try to reference as needed by pyinstaller .exes
        try:
            base_path = sys._MEIPASS
        except Exception:
            # At this point, the raw .py is being run, so nothing special is needed for the filepath.
            base_path = os.path.abspath(".")

        # Return the proper path, which will differ if the program is run via its .exe or .py files.
        return os.path.join(base_path, rel_path)
    
    @staticmethod
    def appDataPath (rel_path):
        """Get the AppData path to a persistent resource. Create AppData/VRCAU directory if needed."""
        app_data = os.getenv("APPDATA")
        path = os.path.join(app_data, "VRCAU")

        if not os.path.exists(path):
            os.makedirs(path)
        
        return os.path.join(path, rel_path)
    
class CookieUtils:
    
    @staticmethod
    def store_cookies (cookies, file_name):
        """Locally store a user's cookie data for a smoother login process later."""
        with open(FileUtils.appDataPath(file_name), "wb") as f:
            cookie_list = [c for c in cookies]
            pickle.dump(cookie_list, f)

    @staticmethod
    def load_cookies (file_name):
        """Retrieve locally stored cookies for use in the login process. Returns None if no cookies are found."""
        
        file = FileUtils.appDataPath(file_name)
        
        if not os.path.exists(file):
            return None
        
        with open(file, 'rb') as f:
            cookies = pickle.load(f)

        return cookies