import os
import argparse
import math


def is_image_file(filename):
    return filename.lower().endswith((".png", ".jpg", ".jpeg"))


def run(args):
    image_dir = args.image_dir
    output_dir = args.output_dir
    multi_frame = args.multi_frame

    files = os.listdir(image_dir)
    print(f"Found {len(files)} images in {image_dir}")
    image_dirname = os.path.dirname(image_dir).split("/")[-1]
    print(image_dirname)
    image_files = [file for file in files if is_image_file(file)]
    image_files = sorted(image_files)

    output_file = os.path.join(output_dir, f"{image_dirname}_list.txt")

    image_groups = {}
    # step through files
    for index, file in enumerate(image_files):
        # current index is middle of group
        index_margin = math.floor(multi_frame / 2)
        start_index = index - index_margin
        end_index = index + index_margin + 1
        group = image_files[start_index:end_index]
        # keep group if all frames exist
        if len(group) == multi_frame:
            image_groups[file] = group

    print(f"{len(image_groups)} image groups of length {multi_frame}")

    file_contents = ""
    for file, images in image_groups.items():
        file_contents += f"{' '.join(images)} {file}\n"

    with open(output_file, "w+") as file:
        file.write(file_contents)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Create an images_list.txt from contents of image directory"
    )
    parser.add_argument("--image_dir", default="./images/lud_images/")
    parser.add_argument("--output_dir", default="./img_list/")
    parser.add_argument("--multi_frame", type=int, default=3)

    args = parser.parse_args()

    run(args)
