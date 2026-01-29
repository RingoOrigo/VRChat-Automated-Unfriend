# VRChat Automated Unfriend - Core
# This is where the bulk of the program's logic is.

import vrchatapi
import vrcaui
import sys

from http.cookiejar import Cookie
from vrchatapi.api import authentication_api
from vrchatapi.exceptions import UnauthorizedException
from vrchatapi.models.two_factor_auth_code import TwoFactorAuthCode
from vrchatapi.models.two_factor_email_code import TwoFactorEmailCode

class VRCAU:

    def __init__ (self, username: str = "", password: str = "", save_login: bool = False):
        # Important variables to use throughout the program. As the user must be able to log in, we must use their credentials.
        # The auth token should be stored securely in order to speed up the login process upon future uses.
        # Have the user opt-in to saving their info for this purpose.
        self.username: str = username
        self.password: str = password
        self.auth_code: str = None
        self.token: str = None
        self.save_login: bool = save_login
        self.client = None
        self.auth_client = None
        
        self.current_user = None

    def __initClient (self):
        """Sets a custom User-Agent for the VRChat API client."""
        configuration = vrchatapi.Configuration(
            username = self.username,
            password = self.password
        )

        self.client = vrchatapi.ApiClient(configuration)
        self.client.user_agent = "VRCAU/0.0.0 nathaniel.t.wasko@gmail.com"
        self.auth_client = authentication_api.AuthenticationApi(self.client)

    def login (self):
        """Log in to VRChat via a Selenium Webdriver using the provided credentials."""        

        self.__initClient()

        try:
            # Call currentuser, as this will log you in if not already logged in.
            self.user = self.auth_client.get_current_user()
        except UnauthorizedException as e:
            # Status 200 indicates that MFA is required.
            if e.status == 200:
                raise MFARequirementError(e)
            else:
                raise LoginError()
        except vrchatapi.ApiException as e:
            raise ApiError()

    def authenticate (self, method: str = "code"):
        """Completes the login process via Two-Factor Authentication."""
        if self.auth_code is None:
            vrcaui.UIHandler.showMFA()

        try:
            if method == "code":
                self.auth_client.verify2_fa(two_factor_auth_code=TwoFactorAuthCode(code=self.auth_code))
            else:
                self.auth_client.verify2_fa_email_code(two_factor_email_code=TwoFactorEmailCode(code=self.auth_code))
        except UnauthorizedException as e:
            if e.status == 401:
                vrcaui.UIHandler.showMFA(failed_attempt=True)
            else:
                print("Error verifying 2FA code.")
                raise LoginError()
        except vrchatapi.ApiException as e:
            raise ApiError()

        self.current_user = self.auth_client.get_current_user()
        print(self.current_user)

    def destroy (self):
        """Destroy the current instance and securely save the required data if requested (Data is saved locally)."""
        
        if self.save_login and self.current_user is not None:
            # The user has chosen to save their login info. Save the auth token securely via CookieJar.
            print("TODO: Deal with cookies to allow logging in easier next time.")

        sys.exit()

class MFARequirementError(Exception):
    """An exception to raise when multi-factor authentication is required."""
    def __init__ (self, api_exception):
        super().__init__("Multi-factor authentication is required to log in to this account.")

class LoginError(Exception):
    """An exception to raise when login fails due to incorrect credentials."""
    def __init__ (self):
        super().__init__("Login failed due to incorrect username or password.")

class ApiError(Exception):
    """An exception to raise when an API error occurs."""
    def __init__ (self):
        super().__init__("An error occurred while communicating with the VRChat API.")

if __name__ == "__main__":
    vrcau = VRCAU()
    vrcau.login()
    vrcau.destroy()