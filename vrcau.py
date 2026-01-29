# VRChat Automated Unfriend - Core
# This is where the bulk of the program's logic is.

import webbrowser
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options

class VRCAU:

    def __init__ (self, username: str = "", password: str = "", auth_code: str = "", save_login: bool = False):
        # Important variables to use throughout the program. As the user must be able to log in, we must use their credentials.
        # The auth token should be stored securely in order to speed up the login process upon future uses.
        # Have the user opt-in to saving their info for this purpose.
        self.username: str = username
        self.password: str = password
        self.auth_code: str = auth_code
        self.token: str = None
        self.save_login: bool = save_login
        self.driver = self.__setDriver()

    def __setDriver (self):
        """A private function to determine the proper webdriver to use based on the user's default browser."""
        browserName = webbrowser.__name__

        # Important options to ensure the browser isn't seen by the end user.
        options = Options()
        options.add_argument("--headless=new")

        # Check the default browser's name.
        if browserName.lower() == "chrome":
            # Chrome is the most popular browser, so we will select it if it is available.
            return webdriver.Chrome(options=options)
        # As this program is intended to run on Windows machines, we can assume that Edge is installed.
        return webdriver.Edge(options=options)

    def login (self, ui=None):
        """Log in to VRChat via a Selenium Webdriver using the provided credentials."""
        self.driver.get("https://vrchat.com/home")
        
        login_field = self.driver.find_element(By.ID, "username_email")
        pass_field = self.driver.find_element(By.ID, "password")
        login_button = self.driver.find_element(By.XPATH, '//*[@id="login-form"]/div[5]/button')

        login_field.send_keys(self.username)
        pass_field.send_keys(self.password)
        login_button.click()

        try:
            # Wait until the URL changes from the login page.
            # It will change to either [URL]/home or [URL]/home/twofactorauth
            WebDriverWait(self.driver, 1).until(
                lambda d: d.current_url != "https://vrchat.com/home/login"
            )

            # In this event, 2FA has kicked in. Gracefully handle this.
            # TODO: MAKE THIS INTERFACE WITH THE UI. PROMP FOR 2FA CODE ENTRY.
            if self.driver.current_url.find("twofactorauth") != -1:
                raise MFRequirementError()
        
        except TimeoutException:
            # If the URL does not change, the login has failed.
            raise LoginError()

        self.__testLoop()

    def authenticate (self, ui=None):
        """Complete the login process via multi-factor authentication if necessary."""

        # Open new window to prompt for 2FA code.
        print("TODO: Implement 2FA support!!")
        # next_button = self.driver.find_element(By.XPATH, '//*[@id="app"]/main/div[2]/div[2]/div/form/div/div[3]/button')

        # for i in range(6):
        #     auth_field = self.driver.find_element(By.XPATH, f'//*[@id="app"]/main/div[2]/div[2]/div/form/div/div[2]/div/div[{i + 1}]/input')
        #     auth_field.send_keys(self.auth_code[i])

        # next_button.click()

    def destroy (self):
        """Destroy the current instance and securely save the required data if requested (Data is saved locally)."""
        if self.save_login:
            print("TODO: Implement destroy() function. Safely store token to speed up login process upon next use.")
        else:
            print("TODO: User has selected not to save login info. Deal with this gracefully.")

    def __testLoop (self):
        """A private function to test the program's functionality."""
        while True:
            c = input("Enter c to cancel")
            if c.lower() == "c":
                self.driver.close()
                return

class MFRequirementError(Exception):
    """An exception to raise when multi-factor authentication is required."""
    def __init__ (self):
        super().__init__("Multi-factor authentication is required to log in to this account.")

class LoginError(Exception):
    """An exception to raise when login fails due to incorrect credentials."""
    def __init__ (self):
        super().__init__("Login failed due to incorrect username or password.")

if __name__ == "__main__":
    vrcau = VRCAU()
    vrcau.login()
    vrcau.destroy()