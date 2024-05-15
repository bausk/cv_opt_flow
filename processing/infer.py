import cv2
import numpy as np
from processing.matrix_operations import calculate_rotation_translation


class CompoundVectorInference:
    def __init__(self) -> None:
        self.rotation_angles = []
        self.translation_vectors = []
        self.cumulative_motion_vector = np.array([0.0, 0.0])

    def infer(self, frame: cv2.typing.MatLike):
        vector_field = frame
        rotation_angle, translation_vector = calculate_rotation_translation(vector_field)
        self.rotation_angles.append(rotation_angle)
        self.translation_vectors.append(translation_vector)
        rotation_angle_rad = -np.radians(rotation_angle)
        rotation_matrix = np.array([[np.cos(rotation_angle_rad), -np.sin(rotation_angle_rad)],
                                     [np.sin(rotation_angle_rad), np.cos(rotation_angle_rad)]])
        rotated_vector = np.dot(rotation_matrix, translation_vector)
        self.cumulative_motion_vector = np.dot(rotation_matrix, self.cumulative_motion_vector)
        self.cumulative_motion_vector += translation_vector
        return self.cumulative_motion_vector
