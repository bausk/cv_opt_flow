import cv2
import numpy as np


def visualize_motion(vis, vector):
    vis_vector = vector.astype(int)
    if not np.any(vis_vector):
        return vis
    height, width, _ = vis.shape
    center_point = (width // 2, height // 2)
    vector_point = center_point + vis_vector
    lines = np.int32([[center_point, vector_point]])
    cv2.polylines(vis, lines, 0, color=(255, 255, 0), thickness=2)
    return vis
