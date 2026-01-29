import vrcau, sys, vrcaui
from vrcau import MFARequirementError
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QFile, QIODevice

if __name__ == "__main__":

    # Show the login screen
    UI = vrcaui.UIHandler()
    try:
        UI.showLogin()
    except MFARequirementError as e:
        print("EXCEPTION TEXT BEGINS NOW")
        print(e)