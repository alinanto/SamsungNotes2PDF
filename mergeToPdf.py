import os
import img2pdf

def images_to_pdf(input_dir, output_pdf):
    images = sorted([
        os.path.join(input_dir, f)
        for f in os.listdir(input_dir)
        if f.lower().endswith(".png")
    ])

    if not images:
        raise ValueError("No PNG images found in directory.")

    print(f"Found {len(images)} images")

    with open(output_pdf, "wb") as f:
        f.write(img2pdf.convert(images))

    print(f"PDF saved to: {output_pdf}")


if __name__ == "__main__":
    input_dir = input("Enter image folder path: ").strip()
    output_pdf = os.path.join(input_dir, "output.pdf")

    images_to_pdf(input_dir, output_pdf)