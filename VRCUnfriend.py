#Import all dependencies that are required for the script to run
import selenium, time, webbrowser, getpass

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

browserName = webbrowser.__name__
WEBSITE_PHRASES = ["Online Friends", "Friends Active on the Website", "Offline Friends"]

USER_NAME = input("Please input your VRChat username / email\n")
PASSWORD = getpass.getpass("Please input your VRChat password (this will NEVER be shared).\n")
WHITELISTED_USERS : str= []

print("Please input the usernames of any friends you would like to keep on your friendslist. \nThese are CASE SENSITIVE! Enter one username per line, beginning a new line after each by pressing ENTER.\nIt is recommended to copy and paste the usernames into this console.\nWhen finished, type \"end\" into the console")

whitelistedFriendUsername = ""

while whitelistedFriendUsername != "end":
    whitelistedFriendUsername = input()
    WHITELISTED_USERS.append(whitelistedFriendUsername)

print("Prerequisites completed. ")

if browserName.lower == "firefox":
    browser = webdriver.FireFox()
elif browserName.lower == "chrome":
    browser = webdriver.Chrome()
else:
    browser = webdriver.Edge()

browser.get("https://vrchat.com/login")

time.sleep(2)
browser.find_element(By.NAME, "username_email").send_keys(f"{USER_NAME}")
browser.find_element(By.NAME, "password").send_keys(f"{PASSWORD}" + Keys.RETURN)

time.sleep(2)

try:
    browser.find_element(By.XPATH, '/html/body/div/main/div[2]/div/form/div[3]/input')
    print("Manually input the code sent to your e-mail address (or authenticator app) in order to finish the log-in.")
    i : str = input("Open the friends sidebar, and press 1 when you are finished.\nIf you wish to cancel, simply type \"cancel\" and the program will shut down.\nTHERE IS NO GOING BACK WHEN YOU CONTINUE! \n")
    if i == "1":
        print("Now beginning the unfriending process...")
    if i == "2":
        browser.close
except:
    print("Now beginning the unfriending process...")

upperBound = int(browser.find_element(By.XPATH, '/html/body/div/main/div[2]/div[2]/div/div[3]/div/div[1]/div/div[3]/div[2]').text)

for x in range(1, upperBound + 3):
    friend = browser.find_element(By.XPATH, f'/html/body/div/main/div[2]/div[2]/div/div[3]/div/div[2]/div/div/div/div[{x}]')
    
    try:
        friendName = browser.find_element(By.XPATH, f'/html/body/div/main/div[2]/div[2]/div/div[3]/div/div[2]/div/div/div/div[{x}]/div/div/div/div[1]/a').text

        if (friendName in WEBSITE_PHRASES):
            print("This would have crashed, but I thought ahead :sunglasses: ... You should not have seen this, though...")
        elif (friendName in WHITELISTED_USERS):
            print(f"{friendName} is whitelisted, so they were not unfriended.")
        else:
            browser.find_element(By.XPATH, f'/html/body/div/main/div[2]/div[2]/div/div[3]/div/div[2]/div/div/div/div[{x}]/div/div/div/div[1]/a').click()
            time.sleep(1)
            browser.find_element(By.XPATH, f'/html/body/div/main/div[2]/div[2]/div/div[2]/div/div/div/div[2]/div[2]/div/button[1]').click()
            time.sleep(1)
            browser.find_element(By.XPATH, f'/html/body/div[2]/div/div[1]/div/div/div[3]/div[1]/button').click()
            time.sleep(1)
    except:
        print("This would've crashed, but I thought ahead :sunglasses: ... You should not have seen this")