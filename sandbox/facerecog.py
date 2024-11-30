import os
import face_recognition
from collections import defaultdict
import random_functions as rf

def group_images_by_faces(image_paths):
    """
    Groups images by the faces detected in them.

    Args:
        image_paths (list): List of file paths to the images.

    Returns:
        dict: A dictionary where keys are face IDs and values are lists of image paths
              containing the corresponding face.
    """
    # A dictionary to map face encodings to the images where they appear
    face_groups = defaultdict(list)

    # A list to store all known face encodings and their corresponding image indices
    known_faces = []

    for img_path in image_paths:
        try:
            # Load the image file
            image = face_recognition.load_image_file(img_path)

            # Find all face encodings in the image
            face_encodings = face_recognition.face_encodings(image)

            # Compare each face encoding with known faces
            for face_encoding in face_encodings:
                found_match = False
                for idx, known_face in enumerate(known_faces):
                    # Compare this face encoding with known ones
                    matches = face_recognition.compare_faces([known_face], face_encoding, tolerance=0.6)
                    if matches[0]:
                        face_groups[idx].append(img_path)
                        found_match = True
                        break

                if not found_match:
                    # Add a new face to the known faces
                    known_faces.append(face_encoding)
                    face_groups[len(known_faces) - 1].append(img_path)
        except Exception as e:
            print(f"Error processing image {img_path}: {e}")

    return face_groups


# List of image paths to process
image_paths = 

# Group images by detected faces
grouped_images = group_images_by_faces(image_paths)

# Print the grouped images
for face_id, images in grouped_images.items():
    print(f"Face {face_id} is found in images: {images}")
