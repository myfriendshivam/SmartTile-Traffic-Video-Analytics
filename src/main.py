import argparse
from pathlib import Path

import cv2

from src.video_loader import VideoLoader
from src.tile_generator import TileGenerator


def main():
    parser = argparse.ArgumentParser(
        description="SmartTile Day 1: video extraction and 4x4 tile visualization"
    )
    parser.add_argument("--video", default="data/input/traffic.mp4",
                        help="Path to input traffic video")
    parser.add_argument("--interval", type=int, default=30,
                        help="Extract one frame every N frames")
    parser.add_argument("--max-frames", type=int, default=10,
                        help="Maximum number of frames to extract")
    args = parser.parse_args()

    print("\n========== SMARTTILE ==========")
    print("DAY 1: VIDEO PROCESSING\n")

    with VideoLoader(args.video) as loader:
        metadata = loader.get_metadata()
        print("VIDEO INFORMATION")
        for key, value in metadata.items():
            print(f"{key}: {value}")

        extracted = loader.extract_frames(
            output_dir="data/frames",
            frame_interval=args.interval,
            max_frames=args.max_frames,
        )
        print(f"\nFrames extracted: {extracted}")

    frame_dir = Path("data/frames")
    result_dir = Path("results/frames")
    result_dir.mkdir(parents=True, exist_ok=True)
    image_paths = sorted(frame_dir.glob("*.jpg"))

    if not image_paths:
        raise RuntimeError("No extracted frames found. Check your input video.")

    generator = TileGenerator(rows=4, cols=4)
    processed = 0

    for image_path in image_paths:
        frame = cv2.imread(str(image_path))
        if frame is None:
            print(f"Skipping unreadable image: {image_path}")
            continue

        tiles = generator.generate_tiles(frame)
        visualized = generator.visualize_tiles(frame, tiles)
        output_path = result_dir / f"{image_path.stem}_tiles.jpg"

        if not cv2.imwrite(str(output_path), visualized):
            raise IOError(f"Failed to save: {output_path}")

        processed += 1
        print(f"{image_path.name}: {len(tiles)} tiles generated")

    print(f"\nProcessed frames: {processed}")
    print("Day 1 processing completed.")
    print("Check results/frames/ for tile visualizations.")


if __name__ == "__main__":
    main()
