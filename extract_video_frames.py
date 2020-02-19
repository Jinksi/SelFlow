import os
import argparse
import math
import json
import time
import sys
import subprocess


def printJson(data):
    print(json.dumps(data))
    sys.stdout.flush()
    time.sleep(0.1)


def extract_video_frames(input, output_dir, fps):
    input_filename = os.path.splitext(os.path.basename(input))[0]

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    subprocess.run(
        [
            "ffmpeg",
            "-hide_banner",
            "-i",
            input,
            "-vf",
            f"fps={fps}",
            "-qscale:v",
            "2",
            os.path.join(output_dir, f"{input_filename}_{fps}fps_%06d.jpg"),
        ]
    )
    print("==================")
    print(
        "Video frames extracted to",
        os.path.join(output_dir, f"{input_filename}_{fps}fps_%06d.jpg"),
    )
    print("==================")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract video frames from a video")
    parser.add_argument("--input", default="./videos/video_test.mov/", required=True)
    parser.add_argument("--output_dir", default="./output/video_frames/", required=True)
    parser.add_argument("--fps", default=25, type=int)

    args = parser.parse_args()

    extract_video_frames(args.input, args.output_dir, args.fps)

    # python extract_video_frames.py --input=videos/video_test.mov --output_dir=output/video_frames --fps=25
