# SmartTile — Day 1: Setup and Video Processing

Day 1 implements:
- Video loading and metadata inspection.
- Configurable frame extraction.
- 4 × 4 tile generation (configurable grid).
- Tile boundary and ID visualization.
- Unit tests for tile generation.

## 1. Requirements

- Python 3.10 or newer recommended.
- A short traffic video (MP4 recommended).
- macOS, Linux, or GitHub Codespaces.

## 2. Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

On Windows PowerShell, activate with:

```powershell
.venv\Scripts\Activate.ps1
```

## 3. Add a video

Copy a traffic video to:

```text
data/input/traffic.mp4
```

Use a video you are permitted to use. The video is intentionally not bundled in this ZIP.

## 4. Run

From the SmartTile project root:

```bash
python -m src.main
```

Optional arguments:

```bash
python -m src.main --video data/input/traffic.mp4 --interval 15 --max-frames 20
```

- `--interval`: extract one frame every N source frames.
- `--max-frames`: maximum number of frames to extract.

Extracted frames are saved to `data/frames/`; tile visualizations are saved to `results/frames/`.

## 5. Run tests

```bash
python -m pytest tests/test_day1.py -v
```

The tests cover 4 × 4 tile count, tile dimensions, coordinates, odd image dimensions, invalid frames, and invalid grid settings.

## Project layout

```text
SmartTile/
├── data/
│   ├── input/
│   ├── frames/
│   └── annotations/
├── models/
├── src/
│   ├── video_loader.py
│   ├── tile_generator.py
│   └── main.py
├── experiments/
├── results/
│   ├── frames/
│   ├── videos/
│   └── graphs/
├── tests/
│   └── test_day1.py
├── requirements.txt
└── README.md
```

## Notes

- Ultralytics, Matplotlib, Pandas, and Streamlit are listed for later project days; Day 1 does not download YOLO weights or require a model.
- Do not commit large input videos, extracted frames, or model weights.
- This is the Day 1 implementation only. Motion scoring, adaptive ROI selection, YOLO inference, experiments, and dashboard functionality are planned for later days.
