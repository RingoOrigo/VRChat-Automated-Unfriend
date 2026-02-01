# vrcau.py
# This is where most of the program's inner logic will take place.

import vrchatapi, vrcaui, sys, utils

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

        self.__initClient()
        try:
            cookies = utils.CookieUtils.load_cookies("cookies.vrcau")
            for cookie in cookies:
                self.client.rest_client.cookie_jar.set_cookie(cookie)

            self.cookie_jar = self.client.rest_client.cookie_jar
            self.login(c = True)
        except Exception as e:
            self.cookie_jar = None

    def __initClient (self):
        """Sets a custom User-Agent for the VRChat API client."""
        # In all honesty, this is likely entirely not needed, though I feel I've worked myself into a trap with this function.
        # It doesn't use too much overhead, so I will refactor it out later. It is on the chopping block.
        configuration = vrchatapi.Configuration(
            username = self.username,
            password = self.password
        )

        self.client = vrchatapi.ApiClient(configuration)
        self.client.user_agent = "VRCAU/0.0.0 nathaniel.t.wasko@gmail.com"
        self.auth_client = authentication_api.AuthenticationApi(self.client)

    def login (self, c = False):
        """Log in to VRChat via their API."""        

        self.__initClient()

        if c:
            # Attempt to use cookies to skip the login process.
            if self.cookie_jar is not None:
                try:
                    self.client.rest_client.cookie_jar = self.cookie_jar
                    self.auth_client = authentication_api.AuthenticationApi(self.client)
                    self.current_user = self.auth_client.get_current_user()
                except Exception as e:
                    raise NoCookiesFoundException()
            else:
                raise NoCookiesFoundException()

        try:
            # If the user does not have 2FA enabled, this will return proper data. Otherwise, move to the 2FA prompt.
            self.user = self.auth_client.get_current_user()
            self.cookie_jar = self.client.rest_client.cookie_jar._cookies["api.vrchat.cloud"]["/"]

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

        # If there is no recorded 2FA code yet, prompt the user for one.
        if self.auth_code is None:
            vrcaui.UIHandler.showMFA()

        # As there are two different 2FA methods available to users, perform different functions based on the specified method.
        try:
            if method == "code":
                self.auth_client.verify2_fa(two_factor_auth_code=TwoFactorAuthCode(code=self.auth_code))
            else:
                self.auth_client.verify2_fa_email_code(two_factor_email_code=TwoFactorEmailCode(code=self.auth_code))
        # Handle incorrect auth codes by pulling up the menu a second time.
        except UnauthorizedException as e:
            if e.status == 401:
                vrcaui.UIHandler.showMFA(failed_attempt=True)
            if e.status == 400:
                vrcaui.UIHandler.showMFA(failed_attempt=True)
            else:
                print("Error verifying 2FA code.")
                raise LoginError()
        except vrchatapi.ApiException as e:
            raise ApiError()

        # Now that we can guarantee the user is logged in, set their current information and keep track of their cookies.
        self.current_user = self.auth_client.get_current_user()
        self.cookie_jar = self.client.rest_client.cookie_jar

    def destroy (self):
        """Destroy the current instance and securely save the required data if requested (Data is saved locally)."""
        
        if self.save_login and self.current_user is not None:
            # The user has chosen to save their login info. Save the auth token securely via CookieJar.
            utils.CookieUtils.store_cookies(self.cookie_jar, "cookies.vrcau")

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

class NoCookiesFoundException (Exception):
    """An exception to raise when cookies are unexpectedly not found."""
    def __init__ (self):
        super().__init__("No cookies were found to login with.")