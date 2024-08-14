from fastapi import HTTPException, status
import pandas as pd
import joblib
import service.Connector as CN
from datetime import datetime

model = joblib.load("./Model/expense_forcasting_model.pkl")


def calculate_age(dob):
    today = datetime.today()
    age = today.year - dob.year
    if (today.month, today.day) < (dob.month, dob.day):
        age -= 1
    return age


def load_user_prediction(user_id: int):
    connection = CN.Connector()
    today = datetime.today()
    try:
        query = f"SELECT username,dob,Gender FROM user WHERE user_id={user_id}"
        result = connection.execute(query)
        if result is None or result == []:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail=f"user id Not Found:{str(user_id)}")
        else:
            user = result[0][0]
            dob = result[0][1]
            age = calculate_age(dob)
            gender = result[0][2]
            categories = ['Cosmetic', 'Travel', 'Clothing', 'Electronics', 'Restaurant', 'Market']
            current_month = datetime.today().month
            data = {
                'Gender': [gender] * len(categories),
                'Month': [current_month] * len(categories),
                'Category': categories,
                'Age': [age] * len(categories)
            }

            df = pd.DataFrame(data)
            results = model.predict(df)
            return results.sum()
    except HTTPException as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"error: {str(err)}")


