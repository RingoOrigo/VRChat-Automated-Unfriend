## Quick-Links

- [Feature List](https://github.com/RingoOrigo/VRChat-Automated-Unfriend#features)
- [Usage Guide](https://github.com/RingoOrigo/VRChat-Automated-Unfriend#usage-guide)
- [Dependencies](https://github.com/RingoOrigo/VRChat-Automated-Unfriend#dependencies)
- [Contributing](https://github.com/RingoOrigo/VRChat-Automated-Unfriend#contributing)
- For extra assistance that may not be covered in this readme, ask for help from [Ouroboros](https://discord.gg/e3ffGxdxzM)
# Automatically Unfriend Users on VRChat

#### For what purpose?
It is all too common to have people on VRChat friending others in order to build trust to increase their [Trust Rank](https://docs.vrchat.com/docs/vrchat-safety-and-trust-system#trust-rank) and reach the coveted Trusted User status. 

As a direct result, many users on VRChat have lists of "friends" consisting of hundreds, if not thousands, of users that are barely known or interacted with. Despite this, the process of unfriending hundreds of people at a time is tedious and time-consuming as the fastest way is to click through several prompts on the [VRChat Website](https://vrchat.com/home).

#### I don't want to unadd all of my friends, though!!
VRCU is not made to unfriend absolutely everyone on your friends list. The program has its own system in place to make sure that you keep the people closest to you friended.


# Features

#### Current
*The script is currently incredibly basic*
- Specify users that will not be unfriended by entering their usernames into the program's console.
- Unfriend all users that are not specified to stay friended.

#### Planned
- User-editable config file
- Cleaner EXE build
- GUI
- Make use of VRChat API
    - Have the script rely on the API and its own GUI instead of a browser session opened by itself.

# Usage Guide

1. Download the latest version from the [releases tab](https://github.com/RingoOrigo/VRChat-Automated-Unfriend/releases)
    - Previous releases are not guaranteed to work, so make sure you are always using the latest one.
    - If you are intending on using the VRCU.py file, ensure all dependencies are installed.
2. Run the file and follow the prompts. Below are them in order.
    - `Please input your VRChat username / email`
        - Type in the console your username or email address that you use to log in. This is CASE SENSITIVE!
        - Press enter to proceed.
    - `Please input your VRChat password`
        - Type in the console the password associated with the username you entered previously. This is CASE SENSITIVE!
        - *Your username and password are not stored by this program. They will never be shared.*
        - Press enter to proceed.
    - `Please input the usernames of any friends you would like to keep on your friends list`
        - Go through your current friends list, and choose the friends you wish to keep added. 
        - Paste one username per line (press enter after each username). Usernames are CASE SENSITIVE!
        - Type `end` into the console and press enter when you have entered the username of each friend you wish to keep.
3. Find your 2-Factor Authentication code.
    - These are either found in the inbox of your associated email OR your authenticator app.
    - Enter the code into the website in the browser opened by the program.
    - Ensure that the friends list on the side of the screen is visible.
4. Type the number `1` into the console in order to continue with the unfriending process.
    - There is no going back from this! Typing 1 into the console WILL begin unfriending every user not whitelisted.


# Running the Python File
*This section includes much less hand-holding, as it is tailored to a more technical audience*
### Dependencies
- [Python](https://python.org/downloads)
    - Script originally built using Python 3.10
- [Selenium](https://pypi.org/project/selenium/) 
    - Selenium is the only dependency that must be installed through pip.
    - `pip install -U selenium`

### Running the Python File
1. Open a command line in the python file's directory.
2. `python VRCU.py`
    - Replace `VRCU` with the filename (If you changed it)
3. Follow [Usage Guide](https://github.com/RingoOrigo/VRChat-Automated-Unfriend/edit/main/README.md#usage-guide)

### Building Your Own EXE from the Python File
1. Install [PyInstaller](https://pyinstaller.org/en/stable/)
    - `pip install -U pyinstaller`
2. Open a command line in the python file's directory.
3. `python -m PyInstaller VRCU.py`
    - Replace `VRCU` with the filename (If you changed it)
    
    
# Contributing
You can contribute in a number of ways. Pull requests are recommended and preferred.
