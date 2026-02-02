## Quick-Links

- [Usage Guide](#usage-guide)
- [Frequently Asked Questions](#frequently-asked-questions)
- [Data Privacy](#data-privacy-and-usage)
- [Handling Rate-Limits](#a-note-on-rate-limits)
- [Contribution Guidelines](#contribution-guidelines)

# Automatically Unfriend Users on VRChat with VRCAU

It is all too common to have people on VRChat friending others in order to build trust to increase their [Trust Rank](https://docs.vrchat.com/docs/vrchat-safety-and-trust-system#trust-rank) and reach the coveted Trusted User status. 

As a direct result, many users on VRChat have lists of "friends" consisting of hundreds, if not thousands, of users that are barely known or interacted with. Despite this, the process of unfriending hundreds of people at a time is tedious and time-consuming, as the fastest way is to click through several prompts on the [VRChat Website](https://vrchat.com/home).

# Usage Guide

VRCAU is made to be as intuitive as possible. Below is a simple outline for general use.
1. Download the [latest release](https://github.com/RingoOrigo/VRChat-Automated-Unfriend/releases/latest).
2. Run the file and follow the GUI flow.
    - Screen 1: Log in with your VRChat information. See [VRCAU's Data Policy](#data-privacy-and-usage) if you are concerned about logging in.
    - Screen 2 (Optional): Input your 2FA code (if you have 2FA enabled)
    - Screen 3: Unimplemented as of this time (01.February.2026)

# Frequently Asked Questions
### What data is collected/stored?
Please read the [Data Privacy and Usage](#data-privacy-and-usage) section, as it goes into much more detail, but in general all data used is publicly accesible with the exception of authentication cookies, which are stored locally and used only to prevent the user from being prompted to login several times.
### I encountered this bug/crash/issue! Help!!
Please [open a new issue](https://github.com/RingoOrigo/VRChat-Automated-Unfriend/issues/new) and include as much information about what you are experiencing as possible. Please label the issue appropriately.
### I don't see my question here, can you answer it?
Naturally, as this program is still awaiting an official release, your question likely is not here. This FAQ section will frequently be updated as more and more questions are received, but for pressing matters, please contact me on Discord (@ringoorigo).

# Data Privacy and Usage
Your user information is yours and yours alone. Below is a detailed outline regarding the data used, collected, and stored by VRCAU along with *how* each of those activities occur.
### 1. Session Authentication Data (Cookies)
Cookies make the internet function, and in this case, your cookies are stored *locally* (in your system's application data directory) only when clicking the *Remember Me* button on the program's login screen. This is done to allow the end-user to skip the login process and to prevent making VRChat's API angry.

This is the only data that VRCAU stores for later use, and it can be easily deleted manually at `{data_dir}/VRCAU/cookies.vrcau`.
### 2. Profile Information
In order to personalize the experience of VRCAU, basic profile information is obtained from VRChat's API. For more information on what exactly VRChat's API returns, read the community written documentation for the [get_current_user](https://vrchat.community/reference/get-current-user) API call.

None of this data is stored by VRCAU locally or otherwise.

### 3. Friendship Data
For VRCAU to function, data must be obtained from your VRChat friends list. The most important data is the `last_activity` and `last_login`, which are used to see which friends have been inactive for the longest periods of time. For more information on all of the information VRCAU receives, read the community written documentation for the [get_friends](https://vrchat.community/reference/get-friends) API call.

None of your friends' data is stored by VRCAU locally or otherwise.

# A Note on Rate-Limits
VRChat's API is not intended for use outside of the VRChat company. As such, little is known about exact limits, and consistency is not necessarily guaranteed. In order to protect your account, as well as VRCAU itself, VRCAU will automatically make short pauses if VRChat's API rate-limits it.

# Contribution Guidelines
Contribution is possible through a number of different ways. If you are confident in your ability to fix a problem or implement a new feature yourself, [create a fork](https://github.com/RingoOrigo/VRChat-Automated-Unfriend/fork) and [open a pull request](https://github.com/RingoOrigo/VRChat-Automated-Unfriend/compare/)!

If you wish to otherwise contribute, feel free to [open a new issue](https://github.com/RingoOrigo/VRChat-Automated-Unfriend/issues/new) with the "Enhancement" label, being as detailed as possible with what you wish to contribute.