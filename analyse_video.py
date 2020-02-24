import os
import argparse
import math
import json
import time
import sys
import subprocess

from extract_video_frames import extract_video_frames
from generate_image_list import generate_image_list
from main import run_selfow


def analyse_video(input, output_dir, fps, use_symmetry, multi_frame=3):
    input_filename = os.path.splitext(os.path.basename(input))[0]
    frames_output_dir = os.path.join(output_dir, "frames")
    flow_output_dir = os.path.join(output_dir, "flow")

    # extract frames
    extract_video_frames(input, frames_output_dir, fps)

    # generate image list
    image_list_file = os.path.join(output_dir, f"{input_filename}_list.txt")
    generate_image_list(
        frames_output_dir,
        output_dir,
        multi_frame,
        images=None,
        filename=image_list_file,
    )

    # test model on generated frames and image list
    run_selfow(frames_output_dir, image_list_file, flow_output_dir, use_symmetry)

    # TODO: merge flow frames to video


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract video frames from a video")
    parser.add_argument("--input", default="./videos/video_test.mov/", required=True)
    parser.add_argument("--output_dir", default="./output/video_output/", required=True)
    parser.add_argument("--fps", default=25, type=int)
    parser.add_argument("--use_symmetry", action="store_true")

    args = parser.parse_args()

    analyse_video(args.input, args.output_dir, args.fps, args.use_symmetry)

    # python analyse_video.py --input=videos/video_test.mov --output_dir=output/video_output_25fps --fps=25 --use_symmetry
