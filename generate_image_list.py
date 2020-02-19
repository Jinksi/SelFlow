import os
import argparse
import math
import json
import time
import sys


def printJson(data):
    print(json.dumps(data))
    sys.stdout.flush()
    time.sleep(0.1)


def is_image_file(filename):
    return filename.lower().endswith((".png", ".jpg", ".jpeg"))


def generate_image_list(image_dir, output_dir, multi_frame, images=None, filename=None):

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    if images:
        files = images.split(",")
        print(f"Using {len(files)} images in {image_dir}")
    else:
        files = os.listdir(image_dir)
        print(f"Found {len(files)} images in {image_dir}")

    image_dirname = os.path.dirname(image_dir).split("/")[-1]
    print(image_dirname)
    image_files = [file for file in files if is_image_file(file)]
    image_files = sorted(image_files)

    if filename:
        output_file = filename
    else:
        output_file = os.path.join(output_dir, f"{image_dirname}_list.txt")

    image_groups = {}
    # step through files
    for index, file in enumerate(image_files):
        # current index is middle of group
        index_margin = math.floor(multi_frame / 2)
        start_index = index - index_margin
        end_index = index + index_margin + 1
        group = image_files[start_index:end_index]
        filename = os.path.splitext(os.path.basename(file))[0]
        # keep group if all frames exist
        if len(group) == multi_frame:
            image_groups[filename] = group

    print(f"{len(image_groups)} image groups of length {multi_frame}")

    file_contents = ""
    for file, images in image_groups.items():
        file_contents += f"{' '.join(images)} {file}\n"

    with open(output_file, "w+") as file:
        file.write(file_contents)
        printJson([])
        printJson(["Saved to", output_file])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create an images_list.txt from contents of image directory"
    )
    parser.add_argument("--image_dir", default="./images/lud_images/", required=True)
    parser.add_argument("--output_dir", default="./img_list/", required=True)
    parser.add_argument("--multi_frame", type=int, default=3)
    parser.add_argument("--images")  # list to str e.g. "file1.png,file2.png,..."
    parser.add_argument("--filename")  # custom path to file.txt

    args = parser.parse_args()

    generate_image_list(args.image_dir, args.output_dir, args.multi_frame, args.images)
