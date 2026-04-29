# Save Notes from Samsung Notes into pdf
# Notes created with dark mode (Color inversion) appears correct in the Samsung Notes App
# But they only export into pdf with standard white background. 
# This script uses the samsung notes app in windows or scrcpy (to mirror from android)
# STEP 1: Generate images/screenshots of the note in the app. This will be rendered correctly in dark bg
# STEP 2: To get maximum clarity, the images are taken with maximum zoom (fit to width)
# STEP 3: The images are stiched together to get a full page and then saved in an output folder pagewise.
# STEP 4: The images are then coverted to a pdf. (Separate script - mergeToPdf.py)

# Uses PyAutoGUI to control the GUI and operate the samsung notes app. 
# Can be equalently used with scrcpy with one line modification.
# Just open the relevant notes app, goto your notes, scroll up to the very first page
# Run the script and wait for the process to complete. The output will be in the output folder.

import pyautogui
import time
import os
import cv2
import numpy as np
from datetime import datetime

# ==== CONFIG ====
OUTPUT_DIR = "output"
SCROLL_AMOUNT = -800   # adjust based on your screen
DELAY = 1.0           # delay between actions
MAX_SCROLLS = 1000     # safety limit to prevent infinite scrolling, adjust as needed

# Adjust screen region to get rid of toolbars and scrol bars
# I have already adjusted the values for a notes app that works in windows with following config
# App in reading mode and full screen
# resolution of display is 1920 * 1080
# Adjust the region according to your screen.
# It is mandatory to get rid of toolbar region so that the stiching logic can work correcly
# If you dont want to set this manually, You can use the getScreenRegion.py
# This script helps to set the values of SCREEN_REGION by taking a sample screenshot

SCREEN_REGION = (5,40,1910,880)  # (x, y, w, h) or None for full screen
print(f"Using screen region: {SCREEN_REGION}")
while(True):
    user_input = input("Do you want to change the screen region? (y/n): ").strip().lower()
    if user_input == "y":
        import getScreenRegion as GSR
        SCREEN_REGION = GSR.select_screen_region()
        if SCREEN_REGION is None:
            print("No region selected, using full screen.")
            SCREEN_REGION = None 
        
        break;
    elif user_input == "n":
        print("Using default screen region.")
        break;
    else:
        print("Invalid input!")    

print(f"Final screen region: {SCREEN_REGION}")

# Detect horizontal gray row (single pixel rows)
# The gray rows are the page breaks in the notes. 
# The stiching logic will stitch the images together until it finds a gray row. 
# Once it finds a gray row, it will cut the page and save it to memory and 
# then continue with the remaining part of the image until it finds the next gray row and so on.
# Use getWinColor.py to get the color of the gray row in your notes and set the TARGET_COLOR and COLOR_TOL accordingly.

# TARGET_COLOR = np.array([37, 37, 37])  # BGR (OpenCV uses BGR!)
# TARGET_COLOR = np.array([19, 19, 19])
TARGET_COLOR = np.array([127, 127, 127])
COLOR_TOL = 8   # tolerance per channel (tune 5–15)
ROW_MATCH_RATIO = 0.98  # % of pixels that must match

def is_gray_row(row):
    """
    Detect if a row matches the separator color (#252525) with tolerance.
    """

    # Compute absolute difference per channel
    diff = np.abs(row.astype(np.int16) - TARGET_COLOR)

    # Check if each pixel is within tolerance for all 3 channels
    matches = np.all(diff <= COLOR_TOL, axis=1)

    # Ratio of matching pixels in this row
    match_ratio = np.sum(matches) / len(matches)

    return match_ratio >= ROW_MATCH_RATIO

print(f"Using page divider target color (R,G,B): {TARGET_COLOR} "
      f"with tolerance: {COLOR_TOL} "
      f"and row match ratio: {ROW_MATCH_RATIO}")
while True:
    user_input = input(
        "Do you want to change the page divider TARGET_COLOR? (y/n): ").strip().lower()

    if user_input == "y":
        import getWinColor as GWC
        (r, g, b), _ = GWC.get_color_at_mouse_click()
        TARGET_COLOR = np.array([r, g, b], dtype=np.uint8)
        break

    elif user_input == "n":
        print("Using default TARGET_COLOR region.")
        break

    else:
        print("Invalid input!")

print(f"Final TARGET_COLOR (R,G,B): {TARGET_COLOR}")

now = datetime.now()

# Custom format: Year-Month-Day Hour:Minute:Second
OUTPUT_DIR += now.strftime("_%Y%m%d_T%H%M%ST")

print(f"Output will be saved in: {OUTPUT_DIR}")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ==== STEP 1: Capture Screenshots ====

# If two consecutive screenshots are almost identical → you reached the end.
def is_same_image(img1, img2, threshold=2.0):
    diff = np.mean(np.abs(img1.astype("float") - img2.astype("float")))
    return diff < threshold


images = []
prev_img = None
scroll_count = 0

print("Starting capture in 10 seconds... switch to Samsung Notes")
time.sleep(10)

while True:
    screenshot = pyautogui.screenshot(region=SCREEN_REGION)
    img = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    if prev_img is not None and is_same_image(prev_img, img):
        print("Reached end of document.")
        break

    images.append(img)
    prev_img = img

    scroll_count += 1
    print(f"Captured {scroll_count}")

    if scroll_count >= MAX_SCROLLS:
        print("Safety break triggered.")
        break

    pyautogui.scroll(SCROLL_AMOUNT)
    time.sleep(DELAY)

# ==== STEP 2: Stitch Images ====

# The function tries to find the number of pixels overlapping between two successive screenshots
# When searching for this overlapping width the min_search and max_search parameters are used.
# They should be set appropriately to reduce the time of stiching together
# too wide margin will find the correct overlap but take long time
# too less margin may miss the correct overlap and causes error in stiching together.
# Try to increase scroll to as high as possible and try to reduce min_search to max_search window as low as possible
# you might have to fine tune the min_search, max_search, SCREEN_REGION and SCROLL_AMOUNT parameters 
# to get the stiching logic to work correclty

def find_overlap(img1, img2, min_search=250, max_search=300):
    """
    Find vertical overlap by minimizing pixel difference.
    Much more reliable than template matching for scrolling content.
    """
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    h1 = gray1.shape[0]
    h2 = gray2.shape[0]

    best_offset = 0
    best_score = float("inf")

    # Try different overlap sizes
    for overlap in range(min_search, max_search):
        if overlap > h1 or overlap > h2:
            break

        region1 = gray1[h1 - overlap:h1, :]
        region2 = gray2[:overlap, :]

        # Compute absolute difference
        diff = np.mean(np.abs(region1.astype("float") - region2.astype("float")))

        if diff < best_score:
            best_score = diff
            best_offset = overlap

    return best_offset, best_score

# Detect horizontal gray band
def detect_page_breaks(img, min_band_height=8):
    h, w, _ = img.shape
    cuts = []

    y = 0
    while y < h:
        row = img[y, :, :]

        if is_gray_row(row):
            band_height = 1

            while y + band_height < h and is_gray_row(img[y + band_height, :, :]):
                band_height += 1

            if band_height >= min_band_height:
                cuts.append([y , band_height])

            y += band_height
        else:
            y += 1

    return cuts

# Keeps page count
page_count = 0
page_list = []
page_anomaly_list = []

# Save a page to memory
def save_page(page):
    global page_count

    page_count += 1
    page_list.append([page_count,len(page)])
    if(len(page)<2000):
        page_anomaly_list.append([page_count,len(page)])

    path = os.path.join(OUTPUT_DIR, f"page_{page_count:04d}.png")
    cv2.imwrite(path, page)

    print(f"Saved page {page_count}")

# Takes one screenshot at a time, stiches it until page break
# Saves page to memory after page breaks and then starts again with the remaining page.
 
current_page = images[0]
image_detail = []
B_score_violate_list = []

for i in range(1, len(images)):
    overlap, B_score = find_overlap(current_page, images[i])

    if(B_score > 0.2): # Best overlap score too high, we need to alteast print in summary
        B_score_violate_list.append((i, overlap, B_score))

    image_detail.append((i, overlap, B_score))

    print(f"Image: {i}, Overlap: {overlap}, Score: {B_score}")
    new_part = images[i][overlap:]
    current_page = np.vstack((current_page, new_part))

    # check for page break inside current_page
    cuts = detect_page_breaks(current_page)

    if cuts:
        if(page_count==0 and len(cuts)==1): # Only one cutting expected in the first page.
            cut_y = cuts[0][0]
            cut_Bheight = cuts[0][1] 

            print(f"Cutting first page {page_count+1} upto height {cut_y} with band Height {cut_Bheight} - Page Height: {cut_y}")
            page = current_page[:cut_y]
            
            save_page(page)
            # keep last image for next page
            current_page = images[i]

        elif(page_count>0 and len(cuts)==2): # Two cuts expected in the subsequent pages.
            cut_y = cuts[0][0]
            cut_Bheight = cuts[0][1] 

            end_y = cuts[1][0]
            end_Bheight = cuts[1][1] 

            print(f"Cutting current page {page_count+1} from height {cut_y+cut_Bheight} with band Height {cut_Bheight}")
            print(f"Cutting upto height {end_y} with band Height {end_Bheight}, Page Height: {end_y-cut_y+cut_Bheight}")
            page = current_page[cut_y+cut_Bheight:end_y]
            
            save_page(page)
            # keep last image for next page
            current_page = images[i]
        
        elif(i==len(images)-1 and len(cuts)==1): # processing the very last screenshot. One cut expected.
            cut_y = cuts[0][0]
            cut_Bheight = cuts[0][1] 

            T_height = len(current_page) # total current of current buffer
            print(f"Cutting last page {page_count+1} from height {cut_y+cut_Bheight} with band Height {cut_Bheight} - Page Height{T_height-cut_y+cut_Bheight}")
            page = current_page[cut_y+cut_Bheight:]
            
            save_page(page)
            
        elif(page_count>0 and len(cuts)==1): # Only one cut observed. Continue until two cuts.
            print(f"Continuing page {page_count+1} with one cut observed.")

        else: 
            print(f"Error: More cuts than expected.\nTotal cuts: {len(cuts)}\n{cuts}")
            exit(1)

# ==== STEP 4 : Save convert to pdf ====
pdf_path = os.path.join(OUTPUT_DIR, "output.pdf")

import mergeToPdf as MTP
MTP.images_to_pdf(OUTPUT_DIR, pdf_path)

print()
print("Summary:")
print(f"Number of images processed: {len(images)}")
print(f"Images with B_score > 0.2: {len(B_score_violate_list)}\n{B_score_violate_list}")
print()
print(f"Number of pages saved: {page_count}")
print(f"Pages with height less than 2000 pixels: {len(page_anomaly_list)}\n {page_anomaly_list}")

u_in = input("Do you want to see the details of each image and the page? (y/n): ").strip().lower()
while(True):
    if u_in == "y":
        print("\nImage details (Image Index, Overlap, B_score):")
        for detail in image_detail:
            print(detail)
        
        print("\nPage details (Page number, Height(pixels)):")
        for page_d in page_list:
            print(page_d)
        break;
    elif u_in == "n":
        break;
    else:
        print("Invalid input! Please enter 'y' or 'n'.")