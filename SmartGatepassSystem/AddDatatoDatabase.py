import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://smartgatepass-19cdf-default-rtdb.firebaseio.com/"
})

data = {
    "123456":
        {
            "name": "Jeff Bezos",
            "degree": "MBA",
            "batch": 1964,
            "total_att": "6",
            "grade": "A",
            "school": "SOET",
            "year": "FY",
            "last_attendance_time": "2022-12-11 00:54:34"

        },
    "555333":
        {
            "name": "Christiano Ronaldo",
            "degree": "BBA",
            "batch": 2020,
            "total_att": "6",
            "grade": "C",
            "school": "SIEM",
            "year": "TY",
            "last_attendance_time": "2022-12-11 00:54:34"

        },
    "121022":
        {
            "name": "Kartik Roshan Naidu",
            "degree": "B.Tech C.T.I.S.",
            "batch": 2020,
            "total_att": "6",
            "grade": "A",
            "school": "SOCSE",
            "year": "BE",
            "last_attendance_time": "2022-12-11 00:54:34"

        },
    "654123":
        {
            "name": "Elon Musk",
            "degree": "B.tech",
            "batch": 2020,
            "total_att": "6",
            "grade": "B",
            "school": "SOCSE",
            "year": "BE",
            "last_attendance_time": "2022-12-11 00:54:34"

        }

}
ref = db.reference('Students')


for key, value in data.items():
    ref.child(key).set(value)
