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

def verify_mfa_format (mfa_code: str) -> bool:
    """Verify that the provided MFA code is in the correct format (6 digits)."""
    if len(mfa_code) != 6:
        return False
    if not mfa_code.isdigit():
        return False
    
    return True

def handleMFA (window, client, failed_attempt = False):
    """For users with Multi-Factor Authentication enabled, prompt for the 2FA code and complete the login process."""

    # Load the MFA prompt UI and open it in a second window.
    mfa_ui_file = QFile("interface/mfa.ui")
    loader = QUiLoader()
    mfa_ui_file.close()

    mfa_window = loader.load(mfa_ui_file)
    mfa_window.show()

    if not failed_attempt:
        mfa_window.errorField.setVisible(False)

    # Now connect the submit button to retrieve the 2FA code and continue login.
    button = mfa_window.submitButton
    button.clicked.connect(lambda: authenticateMFA(mfa_window, client))

def authenticateMFA (mfa_window, client):
    """Retrieve the 2FA code from the MFA window and further continue the login process."""
    mfa_code = mfa_window.mfaField.text().strip()
    
    mfa_window.close()

    try:
        if not verify_mfa_format(mfa_code):
            raise vrcau.LoginError()
        
        if client.authenticate(mfa_code):
            print("Login successful! Now to proceed with main functionality...")
    except vrcau.LoginError:
        handleMFA(mfa_window, client, True)

def initCore (window, username: str, password: str, save_login: bool):
    """Initializes the core VRCAU functionality with the provided login info."""
    client = vrcau.VRCAU(username=username, password=password, save_login=save_login)
    
    try:
        client.login()
    except vrcau.MFRequirementError:
        handleMFA(window, client)
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