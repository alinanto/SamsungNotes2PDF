import os

def imagesRenameAndMove(input_dir, output_dir):
    images = sorted([f
        for f in os.listdir(input_dir)
        if f.lower().endswith(".png")
    ])

    existing = sorted([f
        for f in os.listdir(output_dir)
        if f.lower().endswith(".png")
    ])

    for file in images:
        fileIndex = file[-8:-4]
        index = int(fileIndex) + len(existing)

        i_file = os.path.join(input_dir,file)
        o_fName = f"page_{index:04d}.png" 
        o_file = os.path.join(output_dir,o_fName)
        print(f"XCOPY \"{i_file}\" \"{o_file}\" /-I")
        os.system(f"XCOPY \"{i_file}\" \"{o_file}\" /-I")
    


if __name__ == "__main__":
    input_dir = input("Enter input image folder path: ").strip()
    output_dir = input("Enter output image folder path: ").strip()

    imagesRenameAndMove(input_dir, output_dir)
