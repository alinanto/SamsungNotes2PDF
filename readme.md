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
- `Pillow` — image manipulation

---

## Usage

Run the main script:

```bash
python main.py
```

Follow the on-screen instructions.

The script may ask you to:

- position the Samsung Notes window
- select divider colors
- confirm scrolling parameters

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
├── screenshots/
└── stitched/
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