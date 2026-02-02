# vrcaui.py
# This is where all of the GUI processing will take place.

import sys, vrcau, time, random

from utils import FileUtils
from datetime import datetime, timezone, timedelta
from dateutil.relativedelta import relativedelta
from vrchatapi.exceptions import UnauthorizedException, ApiException
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
        self.current_popup = None
        self.unfriend_list = None

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
        self.current_popup.close()
        self.client.auth_code = self.current_popup.mfaField.text().strip()

        try:
            self.client.authenticate()
        except UnauthorizedException as e:
            if e.status == 401:
                self.showMFA(failed_attempt=True)
            else:
                print("Error verifying 2FA code")

        self.showMainWindow()

    def toggleMenuWithIndex (self, menu, index):
        """Enable the specified menu based on the given index"""
        
        if index == 4:
            menu.setVisible(True)
            print()
        else:
            menu.setVisible(False)

    def parseUnfriendList (self, friends, text_display, cutoff_index, selected_date):
        """Parse what friends will be removed, and update the preview list accordingly."""
        cutoff_date = datetime.now(timezone.utc)
        self.unfriend_list = []

        match cutoff_index:
            case 0: # User selects past day
                cutoff_date = cutoff_date - timedelta(hours = 24)
            case 1: # User selects past week
                cutoff_date = cutoff_date - timedelta(weeks = 1)
            case 2: # User selects past month. Use relativedelta to account for months like february without much effort
                cutoff_date = cutoff_date - relativedelta(months = 1)
            case 3: # User selects past year
                cutoff_date = cutoff_date - relativedelta(years = 1)
            case 4:
                py_date = selected_date.startOfDay().toPython()
                cutoff_date = py_date.replace(tzinfo = timezone.utc)

        # Loop through all friends and add them to the unfriend list if they do not meet the specified recent activity.
        for friend in friends:
            last_activity_time = friend.last_activity
            if last_activity_time < cutoff_date:
                self.unfriend_list.append(friend)
        
        # Update the list of users that will be unfriended.
        unfriend_parsed_text = ""
        for friend in self.unfriend_list:
            unfriend_parsed_text += f"{friend.display_name}\n"

        text_display.setText(unfriend_parsed_text)

    def deny (self):
        """Perform the required logic if the user denies the unfriending confirmation"""
        self.current_popup.close()

    def confirm (self):
        """Perform the required logic if the user confirms the unfriending confirmation"""
        self.current_popup.close()
        limit_break = 1
        
        i = 0
        while i < len(self.unfriend_list):
            try:
                self.client.unfriend(self.unfriend_list[i].id)
                i += 1
            except ApiException as e:
                if e.status == 429:
                    time.sleep((2 ** limit_break) + random.uniform(0, 2))
                    limit_break += 1
                    continue

    def promptConfirmationDialog (self):
        """Show confirmation dialog for unfriending the specified users. Proceed to unfriending phase after confirmation."""
        self.current_popup.show()

        confirm_button = self.current_popup.confirmButton
        deny_button = self.current_popup.denyButton

        deny_button.clicked.connect(lambda: self.deny())
        confirm_button.clicked.connect(lambda: self.confirm())

    def showMainWindow (self):
        """Display the main window of the program"""

        # Get lists of online and offline friends to later combine.
        # While online friends are not necessary if unfriending based on inactivity, they will have a use later as the program expands.
        offlineFriends = self.client.getFriends(offline = True)
        onlineFriends = self.client.getFriends()

        friends = offlineFriends + onlineFriends

        # Load both the main UI and options files.
        main_ui_file = QFile("interface/main.ui")
        confirm_ui_file = QFile("interface/confirm.ui")

        # Ready each of them to be shown at any moment.
        self.window = self.loader.load(main_ui_file)
        self.current_popup = self.loader.load(confirm_ui_file)
        
        # Keep track of certain on-screen fields.
        date_select = self.window.dateBox
        drop_down_menu = self.window.dropdownBox
        parse_button = self.window.parseButton
        unfriend_button = self.window.unfriendButton
        parsed_list_text = self.window.parsedListText

        date_select.setVisible(False)
        drop_down_menu.currentIndexChanged.connect(lambda: self.toggleMenuWithIndex(date_select, drop_down_menu.currentIndex()))
        parse_button.clicked.connect(lambda: self.parseUnfriendList(friends, parsed_list_text, drop_down_menu.currentIndex(), date_select.date()))
        unfriend_button.clicked.connect(lambda: self.promptConfirmationDialog())

        # Show the main UI. Only open options later.
        self.window.show()

        sys.exit(self.app.exec())

    def showMFA (self, failed_attempt = False):
        """Prompt for 2FA code and continue the login process."""

        mfa_ui_file = QFile(FileUtils.resource_path("interface/mfa.ui"))
        self.current_popup = self.loader.load(mfa_ui_file)
        self.current_popup.show()

        if not failed_attempt:
            self.current_popup.errorField.setVisible(False)

        button = self.current_popup.submitButton
        button.clicked.connect(lambda: self.setAuthInfo())