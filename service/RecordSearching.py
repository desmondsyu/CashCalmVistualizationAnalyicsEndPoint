from typing import Type, List, Tuple

from fastapi import HTTPException, status
import service.Connector as CN
from datetime import datetime
import service.Class as Class


def moth_in_list_in_range(from_year: int, from_month: int, to_year, to_month: int) -> list[datetime]:
    if from_month not in range(1, 13) or to_month not in range(1, 13):
        raise HTTPException(status_code=400, detail="Invalid month. Month should be between 1 and 12.")
    if from_year > to_year or (from_year == to_year and from_month > to_month):
        raise HTTPException(status_code=400,
                            detail="Invalid date range. Ensure the 'from' date is before or equal to the 'to' date.")
    if from_year > datetime.today().year or to_year > datetime.today().year:
        raise HTTPException(status_code=400, detail="Invalid year.")
    month_list = list()
    start_date = datetime(year=from_year, month=from_month, day=1)
    end_date = datetime(year=to_year, month=to_month, day=1)
    while start_date <= end_date:
        month_list.append(start_date)
        if start_date.month == 12:
            start_date = datetime(year=start_date.year + 1, month=1, day=1)
        else:
            start_date = datetime(year=start_date.year, month=start_date.month + 1, day=1)

    return month_list


def covert_date(date: datetime) -> tuple[datetime, datetime]:
    start_of_month = date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if date.month == 12:
        end_of_month = start_of_month.replace(year=date.year + 1, month=1)
    else:
        end_of_month = start_of_month.replace(month=date.month + 1)
    return start_of_month, end_of_month


def load_monthly_spending_or_income(user_id: int, search_datetime: datetime) -> list:
    connection = CN.Connector()
    try:
        start_of_month, end_of_month = covert_date(search_datetime)
        query = (
            f"SELECT "
            f"SUM(CASE WHEN tg.type_id = 1 THEN t.AMOUNT ELSE 0 END) AS sum_amount_Income, "
            f"SUM(CASE WHEN tg.type_id = 2 THEN t.AMOUNT ELSE 0 END) AS sum_amount_Expense "
            f"FROM transaction t "
            f"JOIN transaction_group tg ON t.tran_group_id = tg.id "
            f"WHERE t.user_id = '{user_id}' "
            f"AND t.transaction_date >= '{start_of_month}' "
            f"AND t.transaction_date < '{end_of_month}'"
        )
        outcome = connection.execute(query)
        result = list()
        result.append(float(outcome[0][0])) if outcome[0][0] is not None else result.append(0)
        result.append(float(outcome[0][1])) if outcome[0][1] is not None else result.append(0)
        return result

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"{e}")


def month_break_down_in_group(year: int, month: int, user_id: int) -> List[Class.GROUP_SPENDING_IN_MONTH]:
    if month not in range(1, 13):
        raise HTTPException(status_code=400, detail="Invalid month. Month should be between 1 and 12.")

    try:
        start_date = datetime(year=year, month=month, day=1)
        start_of_month, end_of_month = covert_date(start_date)
        query = """
            SELECT tg.name AS GroupName, SUM(t.amount) AS Amount
            FROM transaction t
            JOIN financial_system.transaction_group tg
            ON t.tran_group_id = tg.id
            WHERE tg.type_id = 2
            AND t.transaction_date >= %s
            AND t.transaction_date < %s
            AND t.user_id = '%s'
            GROUP BY tg.name
        """
        connection = CN.Connector()
        result = connection.execute(query, (start_of_month, end_of_month, user_id))

        data = []
        for row in result:
            group_spending = Class.GROUP_SPENDING_IN_MONTH(
                group_name=row[0],
                Amount=float(row[1])
            )
            data.append(group_spending)

        return data

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))