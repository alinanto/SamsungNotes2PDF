from pathlib import Path
import shutil

# Set this to your master folder path
MASTER_FOLDER = r"C:\Users\alina\OneDrive\Projects\salvageNotes"

master_path = Path(MASTER_FOLDER)

# Loop through all folders inside master folder
for folder in master_path.iterdir():
    if folder.is_dir():
        source_pdf = folder / "output.pdf"

        # Check if output.pdf exists
        if source_pdf.exists():
            # Rename to folder name.pdf
            destination_pdf = master_path / f"{folder.name}.pdf"

            # Copy file
            shutil.copy2(source_pdf, destination_pdf)

            print(f"Copied: {source_pdf} -> {destination_pdf}")
        else:
            print(f"No output.pdf in: {folder.name}")

print("Done.")