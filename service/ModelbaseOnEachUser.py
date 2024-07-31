from fastapi import HTTPException, status
import pandas as pd
import joblib
import service.Connector as CN
from datetime import datetime

model = joblib.load("service/Model/expense_forcasting_model.pkl")


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
            gender = result[0][2]
            data = {
                'Gender': ['M', 'M', 'M', 'M', 'M', 'M'],
                'Month': [datetime.today().month, datetime.today().month, datetime.today().month,
                          datetime.today().month, datetime.today().month,
                          datetime.today().month],
                'Category': ['Cosmetic', 'Travel', 'Clothing', 'Electronics', 'Restaurant', 'Market'],
                'Age': [34, 34, 34, 34, 34, 34]
            }
            df = pd.DataFrame(data)
            results = model.predict(df)
            return results.sum()
    except HTTPException as err:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"error: {str(err)}")
def load_monthly_sepnding(user_id: int):

    connection = CN.Connector()
    try:
        current_datetime = datetime.now()
        start_of_month = current_datetime.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        if current_datetime.month == 12:
            end_of_month = start_of_month.replace(year=current_datetime.year + 1, month=1)
        else:
            end_of_month = start_of_month.replace(month=current_datetime.month + 1)

        # Define query for the current month spending
        query_current_spending = (
            f"SELECT SUM(AMOUNT) FROM transaction "
            f"WHERE user_id = '{user_id}' "
            f"AND transaction_date >= '{start_of_month}' "
            f"AND transaction_date < '{end_of_month}' "
            f"AND TYPE_ID = 2"
        )

        current_spending = connection.execute(query_current_spending)
        return current_spending
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"{e}")
