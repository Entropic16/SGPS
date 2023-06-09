import os
import pickle
import cv2
import face_recognition
import numpy as np
import cvzone
import firebase_admin
from firebase_admin import credentials, storage
from firebase_admin import db
from datetime import datetime

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://smartgatepass-19cdf-default-rtdb.firebaseio.com/",
    'storageBucket': "smartgatepass-19cdf.appspot.com"
})

bucket = storage.bucket()

cap = cv2.VideoCapture(0)
cap.set(2, 640)
cap.set(3, 480)

imgBackground = cv2.imread('Resources/NewUI.png')

# Importing the mode images into a list
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = []

for path in modePathList:
    imgModeList.append(cv2.imread(os.path.join(folderModePath, path)))
# print(len(imgModeList))

# Load the encoding file
print("Loading the Encode file...")
file = open('EncodeFile.p', 'rb')
encodeListKnownWithIds = pickle.load(file)
file.close()
encodeListKnown, studentIds = encodeListKnownWithIds
# print(studentIds)             #testing
print("Encode File Loaded")

modeType = 0
counter = 0
id = -1
imgStudent = []

while True:
    success, img = cap.read()

    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    # (img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    faceCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

    imgBackground[199:199 + 480, 63:63 + 640] = img
    imgBackground[40:40 + 639, 825:825 + 405] = imgModeList[modeType]
    if faceCurFrame:
        for encodeFace, faceLoc in zip(encodeCurFrame, faceCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
            print("FaceDis", faceDis)
            print("matches", matches)

            matchIndex = np.argmin(faceDis)
            print("Match Index", matchIndex)

            if matches[matchIndex]:
                print("Known Face Detected")
                print(studentIds[matchIndex])
                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                bbox = 55 + x1, 162 + y1, x2 - x1, y2 - y1
                imgBackground = cvzone.cornerRect(imgBackground, bbox, rt=0)
                id = studentIds[matchIndex]
                print(id)

                if counter == 0:
                    cvzone.putTextRect(imgBackground, "Loading", (275, 400))
                    cv2.imshow("Face recognition", imgBackground)
                    cv2.waitKey(1)
                    counter = 1
                    modeType = 1

        if counter != 0:

            if counter == 1:
                # Getting the data
                studentInfo = db.reference(f'Students/{id}').get()
                print(studentInfo)
                # Getting image from the storage database
                blob = bucket.get_blob(f'Images/{id}.png')
                array = np.frombuffer(blob.download_as_string(), np.uint8)
                imgStudent = cv2.imdecode(array, cv2.COLOR_BGRA2RGB)
                # update data of the students
                datetimeObject = datetime.strptime(studentInfo['last_attendance_time'], "%Y-%m-%d %H:%M:%S")
                secondsElapsed = (datetime.now()-datetimeObject).total_seconds()
                print(secondsElapsed)

                if secondsElapsed > 20:
                    ref = db.reference(f'Students/{id}')
                    total_att = int(studentInfo['total_att'])
                    total_att += 1
                    studentInfo['total_att'] = str(total_att)
                    ref.child('total_att').set(studentInfo['total_att'])
                    # studentInfo['total_att'] += 1
                    # ref.child('total_att').set(studentInfo['total_att'])
                    ref.child('last_attendance_time').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    modeType = 3
                    counter = 0
                    imgBackground[40:40 + 639, 825:825 + 405] = imgModeList[modeType]

            if modeType != 3:


                if 10 < counter < 20:
                    modeType = 2

                imgBackground[40:40 + 639, 825:825 + 405] = imgModeList[modeType]

                if counter <= 10:
                    (w, h), _ = cv2.getTextSize(studentInfo['name'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (405 - w) // 2
                    cv2.putText(imgBackground, str(studentInfo['name']), (837 + offset, 360),
                                cv2.FONT_HERSHEY_COMPLEX, 0.9, (0, 0, 0), 1)

                    (w, h), _ = cv2.getTextSize(studentInfo['degree'], cv2.FONT_HERSHEY_COMPLEX, 1, 1)
                    offset = (395 - w) // 2
                    cv2.putText(imgBackground, str(studentInfo['degree']), (850 + offset, 385),
                                cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0), 1)

                    cv2.putText(imgBackground, str(studentInfo['total_att']), (860, 75),
                                cv2.FONT_HERSHEY_COMPLEX, 0.9, (0, 0, 0), 1)
                    cv2.putText(imgBackground, str(id), (989, 458),
                                cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(studentInfo['school']), (989, 506),
                                cv2.FONT_HERSHEY_COMPLEX, 0.8, (255, 255, 255), 1)
                    cv2.putText(imgBackground, str(studentInfo['batch']), (1140, 645),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 0), 1)
                    cv2.putText(imgBackground, str(studentInfo['year']), (1047, 645),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 0), 1)
                    cv2.putText(imgBackground, str(studentInfo['grade']), (950, 645),
                                cv2.FONT_HERSHEY_COMPLEX, 0.6, (0, 0, 0), 1)

                    imgBackground[159:159+154, 950:950+154] = imgStudent

                counter += 1

                if counter >= 20:
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    imgStudent = []
                    imgBackground[40:40 + 639, 825:825 + 405] = imgModeList[modeType]
    else:
        modeType = 0
        counter = 0
    # cv2.imshow("Webcam", img)
    cv2.imshow("Face recognition", imgBackground)
    # cv2.waitKey(1)

# Hit 'q' on the keyboard to quit!
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release handle to the webcam
imgBackground.release()
cv2.destroyAllWindows()
