import pyautogui
import pyperclip


def readInventory(client):
    tab_selected_color = [117, 40, 30]
    if pyautogui.pixelMatchesColor(client.getX(0.7849196538936959), client.getY(0.6254681647940075), tab_selected_color, tolerance=10):
        return 'On items tab.'
    elif pyautogui.pixelMatchesColor(client.getX(0.8714462299134734), client.getY(0.6254681647940075), tab_selected_color, tolerance=10):
        return 'On prayer tab.'
    else:
        return 'On unknown tab.'


def readPassword():  # Reads password from the password.txt then copies it to the clipboard.
    with open('password.txt', 'r') as reader:
        pyperclip.copy(reader.readline())
    print('Read password from file.')


def login(client):  # Takes control of the mouse and keyboard to login to Runelite.
    print('Beginning login script.')
    client.updateClient()
    client.setFocus()
    existing_user_box_on_screen = [19, 20, 21]
    if pyautogui.pixelMatchesColor(client.getX(0.48825710754017304), client.getY(0.4101123595505618), existing_user_box_on_screen, tolerance=10):
        print("Clicking \"Existing user\" box.")
        pyautogui.click(client.getX(0.48825710754017304), client.getY(0.4101123595505618), interval=1)
    pyautogui.click(client.getX(.4326328801), client.getY(.4588014981), interval=1)
    pyautogui.keyDown('ctrl')
    pyautogui.press('v')
    pyautogui.keyUp('ctrl')
    print('Login complete.')
