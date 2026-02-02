# vrcau.py
# This is where most of the program's inner logic will take place.

import vrchatapi, vrcaui, sys, utils, time, random

from vrchatapi.api import authentication_api, friends_api
from vrchatapi.exceptions import UnauthorizedException, ApiException
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

    def getFriends (self, offline = False):
        """Parse through the friends list of the current_user, returning an array of all friends."""

        friends_client = friends_api.FriendsApi(self.client)
        # Define the number of friends that need to be retrieved. This is important as only up to 100 can be obtained at a time.
        num_friends = len(self.current_user.offline_friends) if offline else (len(self.current_user.active_friends) + len(self.current_user.online_friends))
        parsed_friends = []

        # Request as many friends as possible until all friends have been retrieved.
        i = 0
        limit_break = 1 # Final Fantasy reference!
        while i < num_friends:
            # Wrap logic in try/except to account for the likely possibility of ratelimits.
            try:
                # n = 100 is the largest possible value that VRChat's API will accept.
                # offset = i prevents retrieving the same friend multiple times by setting the new response to start listing where the last one stopped.
                friends = friends_client.get_friends(offset = i, n = 100, offline = offline)

                i += 100

                # Place each friend in the parsed_friends list.
                for friend in friends:
                    parsed_friends.append(friend)

            except ApiException as e:
                # Check for ratelimit code.
                if e.status == 429:
                    # Sleep the thread for an exponentially increasing amount of time each time a ratelimit is encountered.
                    time.sleep((2 ** limit_break) + random.uniform(0, 1))
                    limit_break += 1
                    # Return to the start of the loop
                    continue
                else:
                    print(f"I have no idea what happened. Please inform me on discord @ringoorigo\nCode: {e.status}\n{e.reason}")

        return parsed_friends
    
    def unfriend (self, user_id):
        """Unfriend the provided user. Returns true if user was successfully unfriended, false if otherwise, and an exception if ratelimited."""
        friends_client = friends_api.FriendsApi(self.client)
        
        # Wrap logic in try/except in case of API Errors or ratelimits.
        try:
            friends_client.unfriend(user_id)
        # If an exception is encountered, either return false or raise a ratelimit exception to be handled in parent function.
        except ApiException as e:
            match(e.status):
                case 400:
                    return False
                case 401:
                    return False
                case 429:
                    raise e

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