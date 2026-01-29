import vrcau
import sys

from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QFile, QIODevice

def getLoginInfo (window):
    """Reads user input from app upon pressing the login button."""
    username = window.usernameField.text().strip()
    password = window.passwordField.text().strip()
    save_login = window.rememberMeBox.isChecked()

    initCore(window, username, password, save_login)

def initCore (window, username: str, password: str, save_login: bool):
    """Initializes the core VRCAU functionality with the provided login info."""
    client = vrcau.VRCAU(username=username, password=password, save_login=save_login)
    
    try:
        client.login(ui = window)
    except vrcau.MFRequirementError:
        client.authenticate(ui = window)
    except vrcau.LoginError:
        client.destroy()
        window.errorField.setVisible(True)
        return

if __name__ == "__main__":

    # Initialize the login screen.
    app = QApplication(sys.argv)
    ui_file = QFile("interface/login.ui")
    loader = QUiLoader()
    ui_file.close()

    # Show the login screen.
    window = loader.load(ui_file)
    window.show()
    
    # Connect the login button to the info retrieval function.
    login_button = window.loginButton
    login_button.clicked.connect(lambda: getLoginInfo(window))

    # Ready the error text field
    window.errorField.setVisible(False)

    sys.exit(app.exec())