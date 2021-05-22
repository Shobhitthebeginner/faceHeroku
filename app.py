import flask
from flask import request
from flask import jsonify
import face_recognition
from datetime import datetime
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import urllib
import urllib.request
import numpy as np
import pyrebase
import os
import cv2
from PIL import Image
import requests
from io import BytesIO
import requests
from PIL import Image
from io import BytesIO
import numpy as np
config = {
    "type": "service_account",
    "project_id": "image-23704",
    "private_key_id": "3356ea3be1eacd942f2e46b16924c2fc1d821dd1",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDI1Nxc9eHSPeYB\nSNfMWzkKuEQU6YknVm6OtT8zghD84sZ3GHFmGs2QsHRjTdxj6fSwRoYnPnemUB/M\npDjDotKNjbni4KFkqB69gQhTWxJeREZtjsLfWhtxCaSEH0bbzMWFpEkxl5ds8FiR\npq9f5p4gGs1cMTlURlsEzixE/Ue1tnf9+pBKerqy7OzAWXLgbPaqHv6BMPqBwKHS\nwqftXlBy6idxRM+4BV5gzHD9ASdms1rvsOzOfog6SURmbgEtuURzr6s5AUOwutut\npmPu3sjeR6aPLzB4e6H30MzIYT60cxQuFAYyBSJ+8dRQUoqsS6qKwXULwl85epvY\nmC8DK0jlAgMBAAECggEABYYWnwQSkxjlWMyyrKn0dg8vvcukD5iPOl9rGm6c1Zp4\npoKqxBJ7QUsKxc+FmJtkTqDDjRz6CXFiqsoaeXSnH07+7JSdtFTQYcUaBFrHzoWe\nJ8BnXp0dBcbfnqE47pzOaESASBN6J6bhW2y+82G/OkH2uwiWXaZnNZ5TkZZWfp+2\nePD5vbBqi56JuTkZeuu82TVlmMsRoKnnNP6YmZ0nfv6Q9yTHKT3c1WbZCJvOg8sP\nRuo7ZPsAqPWcBKO2F6N9VGij7xWV84gqaAD/k9s/337kvr1c9+cfWmkI7TY19g3h\n7b2ltbBBQ/PAS2ZcHfAsNhC3ub5l34fbJRaaJOeo8wKBgQD9R5ZksYOFHo8GMt6K\n6RWYoyY412cZo82JvCBg8lF/cuQYaK+2IU5yB3+7LdopB477XpAkijoTopecnpJx\ngUWImdqCnIZv1yt/bDWzVWLs6y2VLSgbJJgt9XLAiJGdtBo/55996JrjTbQdUlwB\nvjXorJhW7rbifjD8ESucV3jerwKBgQDK/RAdt74gbYM3oLYGE4GIVno46eRFrDW9\nF4wPuV9Xt8KJ7mW1EbIM/XGmM+LK3agoWm4k0bNVfau7S/XQ7x+Z4BOISVMPyzpR\newwm6IwOAVFpdD9kmmqyAD0gjmKfh4F0OVYDvoF+F4TZwFBjbELyGNgC77V2p2CE\nNh8uiUyWqwKBgAwxbREN5qn67aG7wzDmxa5idE2aORFn7FYsI1bnc3ryOf7e006u\nTct5hvGo5G7DOWPqin/n06HsWuYkUCJ8ua840Ocmx+YMcsCgofkvLCMBs2ESGnMs\nENNtlIemS3RPHlBjQy9ZilNVA03CEEHZOVkpLfBJb655qrwHy5SsNVprAoGBALRn\n8VjYIuwjKInaFayUzXzkjr/ib/TUNvaV5O9cqzYEpat863vf/ES7Q7SZTKlMEtW6\neUXT8fS7OlO+EPzeaVGS6wknUeEpl+0u1QAHkeIonbiBjo3VB5qnx6wVn+V0w0MO\najntqJzuPi5hU5DpeR49ok4JyVdpLsiSaWgsspr9AoGAIsFvGL3HCv73UbUyybWX\n9DLEc8M2bNgOFvOWWRj7NsKTm2zagutz/6DcVgXhI/Uct9xn1FDTblAX5IOwMkXz\noFveCJBeVpQcu11J0M7naEg6buv0mpX7DscAZMT1nP9rnEXwyFDuX3wYPvK0PMHH\nRUotg0rctiv9ps4Mw7/NR4w=\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk-a3tb3@image-23704.iam.gserviceaccount.com",
    "client_id": "116186165584908361579",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-a3tb3%40image-23704"
                            ".iam.gserviceaccount.com "
}

cred = credentials.Certificate(config)
firebase_admin.initialize_app(cred)
db = firestore.client()
user = db.collection('image').document('images').get().to_dict()
Name=list(user.keys())
Urls=list(user.values())
images=[] # containing matrix
classNames=[]
print(Urls)
for i in range(len(Urls)):
    req = urllib.request.urlopen(Urls[i])
    arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
    img = cv2.imdecode(arr, -1)  # 'Load it as it is'
    # cv2.imshow('lalala', img)
    # cv2.waitKey(0)
    images.append(img)
    classNames.append(Name[i])

def findEncodings(images):
    encodeList=[]
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode=face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList
encodeListKnown = findEncodings(images)
def markAttendance(name):
    with open('Attendance.csv','r+') as f:
        myDataList = f.readlines()
        nameList=[]
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')
# imgElon = face_recognition.load_image_file('ImageBasics/Elon musk.jpg')  # loading image
# imgElon = cv2.cvtColor(imgElon,cv2.COLOR_BGR2RGB)          # Converting BGR to RGB

imgTest = face_recognition.load_image_file('vaibhav.jpg')
imgTest = cv2.cvtColor(imgTest,cv2.COLOR_BGR2RGB)
faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
gray = cv2.cvtColor(imgTest, cv2.COLOR_BGR2GRAY)
faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=3,
        minSize=(30, 30)
)

# Finding faces in our image
# while True:
#     faceloc = face_recognition.face_locations(images[0])[0]   # finding face in picture
#     encodeElon = face_recognition.face_encodings(images[0])[0]  # encode the detected face
#     cv2.rectangle(images[0],(faceloc[3],faceloc[0]),(faceloc[1],faceloc[2]),(255,0,255),2)    # detected face location
#
#
# # Finding faces in our test image
#     facelocTest= face_recognition.face_locations(imgTest)[0]   # finding face in picture
#     encodeTest = face_recognition.face_encodings(imgTest)[0]  # encode the detected face
#     cv2.rectangle(imgTest,(facelocTest[3],facelocTest[0]),(facelocTest[1],facelocTest[2]),(255,0,255),2)
#     print(facelocTest)
#     break
#
# # comparing between faces and finding measurements(distance between them)
# # comparing the two images using linear encoding
#
#     results = face_recognition.compare_faces([encodeElon],encodeTest)
#
# # for finding the best match we will calculate the distance
#     faceDis=face_recognition.face_distance([encodeElon],encodeTest)  # lower the faceDis more chances of matching
#     print(results,faceDis)
#     cv2.putText(imgTest,f'{results}{round(faceDis[0],2)}',(10,40),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
#
#     cv2.imshow('Elon Musk',images[0])         # Showing image
#     cv2.imshow('Elon Test',imgTest)
#     cv2.waitKey(0)

i=0
while True:
    for (x, y, w, h) in faces:
        cv2.rectangle(imgTest, (x, y), (x + w, y + h), (0, 255, 0), 2)
        roi_color = imgTest[y:y + h, x:x + w]
        img=roi_color
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        facesCurrFrame = face_recognition.face_locations(imgS)
        encodeCurrFrame = face_recognition.face_encodings(imgS, facesCurrFrame)
        for encodeFace, faceloc in zip(encodeCurrFrame, facesCurrFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            print(faceDis)
            matchIndex = np.argmin(faceDis)
            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                # print(name)
                y1, x2, y2, x1 = faceloc
                y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), 2, cv2.FILLED)
                cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 0), 2)
                markAttendance(name)
        if (cv2.waitKey(20) & 0xFF == ord('q')):
            break

        cv2.imshow('WebCam', img)



