import os, sys

class FileUtils:
    
    @staticmethod
    def resource_path (rel_path):
        """Get the absolute path to a resource"""
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, rel_path)