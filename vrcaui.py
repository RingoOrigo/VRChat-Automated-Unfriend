# vrcaui.py
# This is where all of the GUI processing will take place.

import sys, vrcau

from utils import FileUtils
from vrchatapi.exceptions import UnauthorizedException
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QFile

class UIHandler:
    def __init__ (self):
        self.app = QApplication(sys.argv)
        self.loader = QUiLoader()
        login_ui_file = QFile(FileUtils.resource_path("interface/login.ui"))
        self.window = self.loader.load(login_ui_file)
        self.client = vrcau.VRCAU()
        self.currentPopup = None

    def showLogin (self):
        """Begin the login flow by showing the login screen."""

        if self.client.current_user == None:
            # Proceed to normal login flow if cookies are unavailable or otherwise do not work.
            self.window.show()

            login_button = self.window.loginButton
            login_button.clicked.connect(lambda: self.setLoginInfo())

            # Ready the error text field
            self.window.errorField.setVisible(False)
            
            # Ensure that the destroy function is called when the window closes.
            self.app.setQuitOnLastWindowClosed(False)
            self.app.lastWindowClosed.connect(self.client.destroy)

            sys.exit(self.app.exec())

        # At this point, cookies have been used to successfully log into the app.
        # As it is, thus, not necessary to prompt for 2FA or even login info, just move immediately to the main screen.
        self.showMainWindow()

    def setLoginInfo (self):
        self.client.username = self.window.usernameField.text().strip()
        self.client.password = self.window.passwordField.text().strip()
        self.client.save_login = self.window.rememberMeBox.isChecked()

        # Proceed to login process.
        try:
            self.client.login()
        except vrcau.MFARequirementError as e:
            self.showMFA()
        except vrcau.LoginError:
            self.window.errorField.setVisible(True)

    def setAuthInfo (self):
        self.currentPopup.close()
        self.client.auth_code = self.currentPopup.mfaField.text().strip()

        try:
            self.client.authenticate()
        except UnauthorizedException as e:
            if e.status == 401:
                self.showMFA(failed_attempt=True)
            else:
                print("Error verifying 2FA code")

        self.showMainWindow()

    def showMainWindow (self):
        """Display the main window of the program"""
        user = self.client.current_user
        
        print(f"Hello, {user.display_name}!")
        print(f"You currently have {len(user.friends)} friends.")
        print(f"Of them, \n     {len(user.active_friends)} {"are" if len(user.active_friends) != 1 else "is"} active in some way, \n     {len(user.online_friends)} {"are" if len(user.online_friends) != 1 else "is"} online, and \n     {len(user.offline_friends)} {"are" if len(user.offline_friends) != 1 else "is"} offline!")

        # Get lists of online and offline friends to later combine.
        # While online friends are not necessary if unfriending based on inactivity, they will have a use later as the program expands.
        offlineFriends = self.client.getFriends(offline = True)
        onlineFriends = self.client.getFriends()

        friends = offlineFriends + onlineFriends
        # # Thankfully, via custom classes, separating user info is this easy.
        # friends = self.client.friends
        
        # # Load both the main UI and options files.
        # main_ui_file = QFile("interface/main.ui")
        # # options_ui_file = QFile("interface/options.ui")

        # # Ready each of them to be shown at any moment.
        # self.window = self.loader.load(main_ui_file)
        # # self.currentPopup = self.loader.load(options_ui_file)

        # # Show the main UI. Only open options later.
        # self.window.show()

        # sys.exit(self.app.exec())

    def showMFA (self, failed_attempt = False):
        """Prompt for 2FA code and continue the login process."""

        mfa_ui_file = QFile(FileUtils.resource_path("interface/mfa.ui"))
        self.currentPopup = self.loader.load(mfa_ui_file)
        self.currentPopup.show()

        if not failed_attempt:
            self.currentPopup.errorField.setVisible(False)

        button = self.currentPopup.submitButton
        button.clicked.connect(lambda: self.setAuthInfo())