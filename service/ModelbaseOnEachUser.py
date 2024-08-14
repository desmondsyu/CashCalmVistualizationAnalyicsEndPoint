from fastapi import HTTPException, status
import pandas as pd
import joblib
import service.Connector as CN
from datetime import datetime

model = joblib.load("service/Model/expense_forcasting_model.pkl")


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
        user, dob, gender = result[0]

        missing_attributes = []

        if dob is None:
            missing_attributes.append('dob')
        if gender is None:
            missing_attributes.append('Gender')

        if missing_attributes:
            missing_attrs_str = ', '.join(missing_attributes)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"User {user} does not have complete information: {missing_attrs_str}")

        else:
            age = calculate_age(dob)
            categories = ['Cosmetic', 'Travel', 'Clothing', 'Electronics', 'Restaurant', 'Market']
            current_month = today.month
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


