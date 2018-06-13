from django.shortcuts import render
from PIL import Image, ImageDraw
from django.http import JsonResponse, HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings as djangoSettings

import cv2
import os
import numpy as np

# Create your views here.

class Check(APIView):

    def post(self, request):
        img = request.data['image']
        # name = request.data['name']
        # file = open(djangoSettings.STATIC_ROOT + '/test-data' + name + '.jpg', 'w')
        # file.write(img)



class Load(APIView):

    # list to hold all subject faces
    faces = []
    # list to hold labels for all subjects
    labels = []

    people = ['', 'Suyash']

    def get(self):
        self.prepare_training_data("media")
        return

    def prepare_training_data(self, data_folder_path):
        dirs = os.listdir(data_folder_path)

        # let's go through each directory and read images within it
        for dir_name in dirs:
            # our subject directories start with letter 's' so
            # ignore any non-relevant directories if any
            if not dir_name.startswith("p"):
                continue

            # extract label number of subject from dir_name
            # format of dir name = slabel
            # , so removing letter 's' from dir_name will give us label
            label = int(dir_name.replace("p", ""))

            # build path of directory containing images for current subject subject
            # sample subject_dir_path = "media/p1"
            subject_dir_path = data_folder_path + "/" + dir_name

            # get the images names that are inside the given subject directory
            subject_images_names = os.listdir(subject_dir_path)

            # go through each image name, read image,
            # detect face and add face to list of faces
            for image_name in subject_images_names:

                # ignore system files like .DS_Store
                if image_name.startswith("."):
                    continue

                # build image path
                # sample image path = media/p1/1.jpg
                image_path = subject_dir_path + "/" + image_name

                # read image
                image = cv2.imread(image_path)

                # display an image window to show the image
                cv2.imshow("Training on image...", image)
                cv2.waitKey(100)

                # detect face
                face, rect = self.detect_face(image)

                # STEP 4
                # we will ignore faces that are not detected
                if face is not None:
                    # add face to list of faces
                    self.faces.append(face)
                    # add label for this face
                    self.labels.append(label)
        return self.faces, self.labels

    def detect_face(self, img):
        # convert the test image to gray scale as opencv face detector expects gray images
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # load OpenCV face detector, I am using LBP which is fast
        # there is also a more accurate but slow: Haar classifier
        face_cascade = cv2.CascadeClassifier('opencv-files/lbpcascade_frontalface.xml')

        # Haar classifier
        # face_cascade = cv2.CascadeClassifier('opencv-files/haarcascade_frontalface_alt.xml')

        # let's detect multiscale images(some images may be closer to camera than others)
        # result is a list of faces
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)

        # if no faces are detected then return original img
        if (len(faces) == 0):
            return None, None

        # under the assumption that there will be only one face,
        # extract the face area
        (x, y, w, h) = faces[0]

        # return only the face part of the image
        return gray[y:y + w, x:x + h], faces[0]