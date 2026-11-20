import numpy as np
import pytest

from src.tile_generator import TileGenerator


def test_generates_16_tiles():
    frame = np.zeros((640, 640, 3), dtype=np.uint8)
    tiles = TileGenerator(4, 4).generate_tiles(frame)
    assert len(tiles) == 16


def test_tile_dimensions():
    frame = np.zeros((640, 640, 3), dtype=np.uint8)
    tiles = TileGenerator(4, 4).generate_tiles(frame)
    assert tiles[0]["image"].shape[:2] == (160, 160)


def test_tile_coordinates():
    frame = np.zeros((640, 640, 3), dtype=np.uint8)
    tiles = TileGenerator(4, 4).generate_tiles(frame)
    assert (tiles[0]["x1"], tiles[0]["y1"]) == (0, 0)
    assert (tiles[0]["x2"], tiles[0]["y2"]) == (160, 160)


def test_odd_dimensions_cover_entire_frame():
    frame = np.zeros((641, 643, 3), dtype=np.uint8)
    tiles = TileGenerator(4, 4).generate_tiles(frame)
    assert len(tiles) == 16
    assert tiles[-1]["x2"] == 643
    assert tiles[-1]["y2"] == 641


def test_invalid_frame():
    with pytest.raises(ValueError):
        TileGenerator(4, 4).generate_tiles(None)


def test_invalid_grid():
    with pytest.raises(ValueError):
        TileGenerator(0, 4)
