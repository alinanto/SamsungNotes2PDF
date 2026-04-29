# This script can be used to get the RGB and HEX color values of any pixel on the screen by holding the Ctrl key and clicking on the desired location.
# This is useful for identifying the canvas color of the notes in Samsung Notes,
# which can help in identifying when a page ends and next page begins


import pyautogui
from pynput import mouse, keyboard

def get_color_at_mouse_click():

    ctrl_pressed = False
    r, g, b = -1, -1, -1
    c_X, c_Y = -1, -1

    # Track Ctrl key state
    def on_key_press(key):
        nonlocal ctrl_pressed
        if key in (keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
            ctrl_pressed = True

    def on_key_release(key):
        nonlocal ctrl_pressed
        if key in (keyboard.Key.ctrl_l, keyboard.Key.ctrl_r):
            ctrl_pressed = False

    # Mouse click handler
    def on_click(x, y, button, pressed):
        nonlocal ctrl_pressed, r, g, b, c_X, c_Y
        if pressed and ctrl_pressed:
            c_X, c_Y = x, y
            r,g,b = pyautogui.pixel(x, y)

            return False  # Stop listener after one click
    # Start listeners
    keyboard_listener = keyboard.Listener(
        on_press=on_key_press,
        on_release=on_key_release
    )

    print("Control + L Mouse Click anywhere to identify the color")

    mouse_listener = mouse.Listener(on_click=on_click)

    keyboard_listener.start()
    mouse_listener.start()

    mouse_listener.join()

    keyboard_listener.stop()
    mouse_listener.stop()

    return (r, g, b), (c_X, c_Y)

if __name__ == "__main__":
    (r, g, b), (x, y) = get_color_at_mouse_click()
    
    print(f"\nClicked at ({x}, {y})")
    print(f"RGB: ({r}, {g}, {b})")
    print(f"HEX: #{r:02X}{g:02X}{b:02X}")
    print("-" * 40)
