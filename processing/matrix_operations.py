import cv2
import numpy as np


def calculate_rotation_translation(matrix: np.ndarray):
    # Step 1: Compute the centroid
    # Compute the vector lengths
    vector_lengths = np.linalg.norm(matrix, axis=2)
    # Find the threshold value corresponding to the 90th percentile
    threshold = np.percentile(vector_lengths.flatten(), 90)
    # Create a mask to filter values based on the threshold
    mask = vector_lengths > threshold

    # Apply the mask to the matrix along the last axis
    filtered_matrix = np.where(mask[..., np.newaxis], matrix, np.nan)
    # Calculate the centroid using the filtered matrix
    centroid = np.nanmean(filtered_matrix, axis=(0, 1))
    # End of sparse implementation

    centroid = np.mean(matrix, axis=(0, 1))

    # Step 2: Translate the points to the centroid
    translated_points = matrix - centroid

    # Reshape to treat each vector as a single point
    flattened_points = np.reshape(translated_points, (-1, 2))

    # Step 3: Calculate the covariance matrix
    covariance_matrix = np.cov(flattened_points, rowvar=False)

    # Step 4: Compute the eigenvectors and eigenvalues
    eigenvalues, eigenvectors = np.linalg.eig(covariance_matrix)

    # Step 5: Determine the rotation angle
    rotation_angle = np.arctan2(eigenvectors[1, 0], eigenvectors[0, 0])

    # Step 6: Determine the translation vector
    # translation_vector = centroid - np.dot(centroid, np.array([[np.cos(rotation_angle), -np.sin(rotation_angle)],
    #                                                           [np.sin(rotation_angle), np.cos(rotation_angle)]]))
    rotation_matrix = np.array([[np.cos(rotation_angle), -np.sin(rotation_angle)],
                                 [np.sin(rotation_angle), np.cos(rotation_angle)]])
    translation_vector = centroid - np.dot(rotation_matrix, centroid)
    return rotation_angle, translation_vector
