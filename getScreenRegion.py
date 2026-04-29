# It is mandatory to get rid of toolbar region so that the stiching logic can work correcly
# If you dont want to set this manually, You can use the getScreenRegion.py
# This script helps to set the values of SCREEN_REGION by taking a sample screenshot

# STEP 1 : Take a sample screenshot -
#          User has to navigate to the notes app maually
#          The app display configuration has to be the same that is used with the salvageRegion.py script
#          Make sure to use Reading Mode and Full screen for best performance
# STEP 2 : The script will take a sample screenshot and switch to it's own windows.
#          User has to select the screen region that displays the note using the rectangular selection
# STEP 3:  The app will give the current value of SCREEN_REGION = (x,y,width,height) or (x, y, w, h) or None for full screen
#          Use this value in the salvageNotes.py script and 
import pyautogui
import cv2
import numpy as np
import time

def select_screen_region(delay=10):
    print(f"You have {delay} seconds to switch to Samsung Notes...")
    time.sleep(delay)

    screenshot = pyautogui.screenshot()
    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    clone = img.copy()
    ref_point = []
    cropping = False

    def click_and_crop(event, x, y, flags, param):
        nonlocal ref_point, cropping, img

        if event == cv2.EVENT_LBUTTONDOWN:
            ref_point = [(x, y)]
            cropping = True

        elif event == cv2.EVENT_MOUSEMOVE and cropping:
            temp = clone.copy()
            cv2.rectangle(temp, ref_point[0], (x, y), (0, 255, 0), 2)
            cv2.imshow("Select Region", temp)

        elif event == cv2.EVENT_LBUTTONUP:
            ref_point.append((x, y))
            cropping = False

            cv2.rectangle(img, ref_point[0], ref_point[1], (0, 255, 0), 2)
            cv2.imshow("Select Region", img)

    cv2.namedWindow("Select Region")
    cv2.setMouseCallback("Select Region", click_and_crop)

    print("\nInstructions:")
    print("- Click and drag to select the note area")
    print("- Press 'r' to reset selection")
    print("- Press 'c' to confirm selection")

    while True:
        cv2.imshow("Select Region", img)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("r"):
            img = clone.copy()

        elif key == ord("c"):
            break

    cv2.destroyAllWindows()

    if len(ref_point) != 2:
        print("No region selected")
        return None

    (x1, y1), (x2, y2) = ref_point

    x = min(x1, x2)
    y = min(y1, y2)
    w = abs(x2 - x1)
    h = abs(y2 - y1)

    return (x, y, w, h)

if __name__ == "__main__":
    region = select_screen_region()

    if region is None:
        print("No region selected")
    else:
        print("\n✅ Use this in your main script:")
        print(f"SCREEN_REGION = {region}")