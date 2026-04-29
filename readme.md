# SamsungNotes2PDF

Convert handwritten Samsung Notes into clean, shareable PDFs automatically.

Samsung Notes exports dark-mode notes with a white background in PDFs, which can make handwritten notes difficult to read. This project automates the process of capturing notes directly from the Samsung Notes app (or scrcpy mirror), processing the images, and generating properly stitched PDF outputs with the original dark appearance preserved.

---

## Features

- Automated scrolling and capture of Samsung Notes
- Works with:
  - Samsung Notes on Windows
  - Samsung Notes mirrored through `scrcpy`
- Detects page dividers using RGB color matching
- Automatically stitches screenshots into full pages
- Removes overlapping/repeating regions between captures
- Generates clean PDF exports
- Dark-mode friendly workflow
- Adjustable color tolerance and detection thresholds

---

## Example Workflow

1. Open a note in Samsung Notes
2. Run the script
3. The script:
   - captures screenshots
   - scrolls automatically
   - detects page boundaries
   - stitches images together
   - exports final PDFs

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/alinanto/SamsungNotes2PDF.git
cd SamsungNotes2PDF
```

### 2. Create a virtual environment (recommended)

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

#### Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## Requirements

- Python 3.10+
- Samsung Notes app or `scrcpy`
- A display resolution where the note area is fully visible
- Dark mode notes (recommended)

---

## Main Dependencies

- `opencv-python` — image processing and stitching
- `numpy` — pixel operations
- `pyautogui` — GUI automation and screenshots
- `keyboard` — keyboard event handling
- `pynput` - Handle mouse inputs
- `img2pdf` - Handle image to pdf conversion.

---

## Usage

Run the main script:

```bash
python salvageNotes.py
```

Follow the on-screen instructions.

The script may ask you to:

- `Change the SCREEN_REGION` : If you want to adjust this region of capture (recommended for first time use) type _"y"_ when promted, go to the  the Samsung Notes window (in fullscreen and read mode configuration) and wait for 10 sec. The script will capture an screenshot and open a new window for you to select the screen region. Use mouse to select the rectangular region (avoid toolbar and scroll bar area) and then click c to confirm or r to reset.
- `Select divider colors` : By default the divider color is set to gray, but depending on your color mode it may be different for your use. When the script froms for change, press _"y"_ and then go to the samsung Notes app and press `Ctrl + Left Mouse Buttom` on the divider area to select the page divider color. 
- `Confirm scrolling parameters` : By default scrolling is set to half the page, you can increase this if your resolution is higher than 1980 x 1080. You might need to adjust the `MAX_SEARCH` and `MIN_SEARCH` to speed up the overlap searching function.  

---

## Divider Detection

The script uses RGB color detection instead of arbitrary grayscale matching.

Example divider color:

```python
RGB: (37, 37, 37)
HEX: #252525
```

Thresholds can be adjusted in the script:

```python
COLOR_TOL
ROW_MATCH_RATIO
```

---

## Project Structure

```text
SamsungNotes2PDF/
│
├── main.py
├── requirements.txt
├── output/
```

---

## Known Limitations

- Requires consistent zoom level during capture
- Very large notes may take time to process
- Incorrect divider color settings can affect stitching quality
- UI changes in Samsung Notes may require parameter adjustments

---

## Troubleshooting

### `cv2` not installed

Install OpenCV manually:

```bash
pip install opencv-python
```

### Stitching creates repeated regions

Try adjusting:

- overlap detection threshold
- scroll amount
- divider RGB tolerance

---

## Script Overview

### `salvageNotes.py`

Main automation pipeline.

Responsible for:

- Capturing screenshots from Samsung Notes
- Automatically scrolling through notes
- Detecting page dividers
- Finding overlapping regions between screenshots
- Stitching screenshots into complete pages
- Exporting final PDFs

This is the primary script you run.

---

### `mergeToPdf.py`

Merge PNG images in a folder to a pdf. The main scripts runs this at the end, but can also be used standalone.

```bash
python mergeToPdf.py
Enter image folder path: <output_folder_name>
```

---

### `mergeFolders.py`

Transfers png images in one folder to another folder taking care of the file indexes in both the folders. This is usefull when you have to merge two partially generated image folders. This usually happens when the script detects blank pages in a single note or if the user input is interfering in between a scroll. Once merged you can directly call the mergeToPdf.py to merge the output png images to pdf.

```bash
python mergeFolders.py
Enter input image folder path: <input_folder_name>
Enter output image folder path: <output_folder_name>

python mergeToPdf.py
Enter image folder path: <output_folder_name>
```

---

### `getScreenRegion.py`

The main scripts calls this if you select yes when it promts you to change the SCREEN_REGION. It is advised to do this for the initial setup. You can also run this manually to directly get the values for SCREEN_REGION = ( x ,y , width, height ) and then edit in the main script.

### `getWinColor.py`

Utility script for divider color selection. The main script prompts you if you want to change the divider color. if you select yes, then this script is called. You can also run this script manually to get the RBG color for yourself and edit this in the script(better for converting more than one note)

```bash
python getWinColor.py
```
Used to:

- Detect RGB color values from any screen location
- Capture divider colors using:
  - `Ctrl + Left Mouse Button`
- Help configure:
  - `TARGET_COLOR`
  - `COLOR_TOL`

Useful when Samsung Notes uses a different theme or divider color.

---

### `requirements.txt`

Contains all Python dependencies required for the project.

Install them using:

```bash
pip install -r requirements.txt
```

---

### `output/`

Stores generated outputs:

- stitched images
- exported PDFs

---


### Automation clicks wrong area

Ensure:

- display scaling is set consistently
- Samsung Notes window is fully visible
- no other window overlaps the note area

---

## Future Improvements

- GUI interface
- Automatic OCR export
- Multi-note batch export
- Better overlap detection
- Direct PDF export pipeline
- Auto calibration for divider colors

---

## Contributing

Pull requests and issue reports are welcome.

If you find bugs or have ideas for improvements, open an issue on GitHub.

---

## License

MIT License

---

## Acknowledgements

Inspired by the frustration of Samsung Notes exporting dark-mode handwritten notes with white backgrounds instead of preserving the original appearance.