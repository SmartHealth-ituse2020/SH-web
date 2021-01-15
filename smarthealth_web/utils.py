import csv
import requests
from flask import url_for


req = "http://itu-se2020-smarthealth-pred.herokuapp.com/predict?age={age}&gender={gender}&race={race}&ethnicity={ethnicity}&obesity={obesity}&heart_rate={heart_rate}&d_bp={d_bp}&s_bp={s_bp}&ew={ew}"


def get_prediction(patient_id):
    with open("./external/hospital.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        p = 0
        for row in csv_reader:
            if row[0] == str(patient_id):
                p = 1
                age = row[1]
                if row[2]:
                    gender = 'Female'
                else:
                    gender = 'Male'
                if row[4]:
                    race = 'Asian'
                elif row[5]:
                    race = 'Black'
                elif row[6]:
                    race = 'Native'
                elif row[7]:
                    race = 'Other'
                else:
                    race = 'White'
                if row[9]:
                    ethnicity = 'Hispanic'
                else:
                    ethnicity = 'Nonhispanic'
                obesity = row[11]
                heart_rate = row[12]
                d_bp = row[13]
                s_bp = row[14]
                ew = row[15]
                break
    print(age, gender, race, ethnicity, obesity, heart_rate, d_bp, s_bp, ew)
    if not p:
        return None
    pred = requests.get(req.format(
        age=age,
        gender=gender,
        race=race,
        ethnicity=ethnicity,
        obesity=obesity,
        heart_rate=heart_rate,
        d_bp=d_bp,
        s_bp=s_bp,
        ew=ew,
    )
    )

    return pred.content
