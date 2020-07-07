import glob
import cv2
import os
import face_recognition
import numpy as np
from Detected import Detected


class Camera:
    dirname = os.path.dirname(__file__)
    path = os.path.join(dirname, 'known_people/')

    def __init__(self, video_device=0):
        self.__cap = cv2.VideoCapture(video_device)
        self.__known_face_encodings = []
        self.__known_face_names = []
        self.__face_locations = []
        self.__face_names = []

        self.__initialize_faces()

    def __initialize_faces(self):
        """
        Makes all of encodings for all known faces and keeps
        them in memory for later usage.
        :return: None
        """

        list_of_files = [f for f in glob.glob(f"{Camera.path}*.jpg")]
        number_of_known_faces = len(list_of_files)
        names = list_of_files.copy()

        for i in range(number_of_known_faces):
            globals()['image_{}'.format(i)] = face_recognition.load_image_file(list_of_files[i])
            globals()['image_encoding_{}'.format(i)] = face_recognition.face_encodings(globals()['image_{}'.format(i)])[0]
            self.__known_face_encodings.append(globals()['image_encoding_{}'.format(i)])

            # Create array of known names
            names[i] = names[i].replace("known_people/", "")
            self.__known_face_names.append(names[i])

    def detect(self):
        """
        Detects the faces and returns a bool if the face is known.
        :return: Detected
        """
        face_encodings = []

        success, frame = self.__cap.read()

        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb_small_frame = small_frame[:, :, ::-1]

        if success:
            self.__face_locations = face_recognition.face_locations(rgb_small_frame)
            face_encodings = face_recognition.face_encodings(rgb_small_frame, self.__face_locations)

            if not self.__face_locations:
                return Detected.INVALID

            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(self.__known_face_encodings, face_encoding)

                face_distances = face_recognition.face_distance(self.__known_face_encodings, face_encoding)

                if not face_distances:
                    continue

                best_match_index = np.argmin(face_distances)

                if matches[best_match_index]:
                    return Detected.VALID

                return Detected.INVALID
