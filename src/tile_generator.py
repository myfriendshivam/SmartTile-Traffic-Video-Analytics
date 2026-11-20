import cv2


class TileGenerator:
    """Divide an image into a grid and optionally draw tile boundaries."""

    def __init__(self, rows=4, cols=4):
        if rows < 1 or cols < 1:
            raise ValueError("Rows and columns must be positive")
        self.rows = rows
        self.cols = cols

    def generate_tiles(self, frame):
        if frame is None or getattr(frame, "size", 0) == 0:
            raise ValueError("Invalid input frame")

        height, width = frame.shape[:2]
        tiles = []

        for row in range(self.rows):
            for col in range(self.cols):
                x1 = col * width // self.cols
                x2 = (col + 1) * width // self.cols
                y1 = row * height // self.rows
                y2 = (row + 1) * height // self.rows

                tiles.append({
                    "tile_id": row * self.cols + col,
                    "row": row,
                    "col": col,
                    "x1": x1,
                    "y1": y1,
                    "x2": x2,
                    "y2": y2,
                    "image": frame[y1:y2, x1:x2],
                })
        return tiles

    def visualize_tiles(self, frame, tiles):
        if frame is None or getattr(frame, "size", 0) == 0:
            raise ValueError("Invalid input frame")

        output = frame.copy()
        for tile in tiles:
            x1, y1 = tile["x1"], tile["y1"]
            x2, y2 = tile["x2"], tile["y2"]
            tile_id = tile["tile_id"]

            cv2.rectangle(output, (x1, y1), (x2 - 1, y2 - 1), (0, 255, 0), 2)
            cv2.putText(
                output, f"Tile {tile_id}", (x1 + 8, y1 + 22),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1,
                cv2.LINE_AA
            )
        return output
