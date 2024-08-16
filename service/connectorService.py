from datetime import datetime

from fastapi import HTTPException, status

import service.Interfaces as Class
import service.connector as cn
from service.Interfaces import *


def covert_date(date: datetime) -> tuple[datetime, datetime]:
    start_of_month = date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if date.month == 12:
        end_of_month = start_of_month.replace(year=date.year + 1, month=1)
    else:
        end_of_month = start_of_month.replace(month=date.month + 1)
    return start_of_month, end_of_month


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


def load_monthly_spending_or_income(user_id: int, search_datetime: datetime) -> list:
    connection = cn.Connector()
    try:
        start_of_month, end_of_month = covert_date(search_datetime)
        query = (
            f"SELECT "
            f"SUM(IF(tg.type_id = 1, t.AMOUNT, 0)) AS sum_amount_Income, "
            f"SUM(IF(tg.type_id = 2, t.AMOUNT, 0)) AS sum_amount_Expense "
            f"FROM transaction t "
            f"JOIN transaction_group tg ON t.tran_group_id = tg.id "
            f"WHERE t.user_id = '{user_id}' "
            f"AND t.transaction_date >= '{start_of_month}' "
            f"AND t.transaction_date < '{end_of_month}'"
        )
        results = connection.execute(query)
        return results

    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"{e}")


def month_break_down_in_group(year: int, month: int, user_id: int, in_type: bool) -> list[GROUP_SPENDING] | \
                                                                                     tuple[
                                                                                         list[GROUP_SPENDING],
                                                                                         list[GROUP_SPENDING]]:
    global group_spending, data_Income, data, data_Expense
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
            AND t.transaction_date >= %s
            AND t.transaction_date < %s
            AND t.user_id = '%s'
            GROUP BY tg.name
        """
        connection = cn.Connector()
        result = connection.execute(query, (start_of_month, end_of_month, user_id))
        data_Income = []
        data_Expense = []
        for row in result:
            if float(row[1]) < 0:
                group_spending = Class.GROUP_SPENDING(
                    date=f"{start_date.year}/{start_of_month.month}",
                    group_name=row[0],
                    amount=float(row[1]) * -1,
                    type="Expense"
                )
                data_Expense.append(group_spending)
                continue
            else:
                group_spending = Class.GROUP_SPENDING(
                    date=f"{start_date.year}/{start_of_month.month}",
                    group_name=row[0],
                    amount=float(row[1]),
                    type="Income"
                )
                data_Income.append(group_spending)
        if in_type:
            return data_Income, data_Expense
        else:
            return data_Income + data_Expense
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


def month_breakdown_in_label(year: int, month: int, user_id: int, historical: bool) -> list[LABEL_SPENDING]:
    if month not in range(1, 13):
        raise HTTPException(status_code=400, detail="Invalid month. Month should be between 1 and 12.")
    try:
        data = list()
        start_date = datetime(year=year, month=month, day=1)
        start_of_month, end_of_month = covert_date(start_date)
        query = f"""
            SELECT l.name AS Label_Name, SUM(t.amount) AS Amount
            FROM transaction t
            JOIN financial_system.label l ON t.label_id = l.id
            WHERE t.transaction_date < %s
            AND t.user_id = {user_id}
        """

        params = [end_of_month]

        if not historical:
            query += "AND t.transaction_date >= %s "
            params.append(start_of_month)

        query += "GROUP BY l.name"
        connection = cn.Connector()
        result = connection.execute(query, params)

        for row in result:
            label_spending = Class.LABEL_SPENDING(
                label_name=row[0],
                amount=float(row[1]),
                date=f"{start_date.year}/{start_of_month.month}",
            )
            data.append(label_spending)
        return data
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


def label_break_down(user_id: int, label_id: int) -> list[GROUP_SPENDING]:
    data = []
    query = f"""
         SELECT tg.name AS GroupName, SUM(t.amount) AS Amount
         FROM transaction t
         JOIN financial_system.transaction_group tg
         ON t.tran_group_id = tg.id
         AND t.user_id = {user_id}
         AND t.label_id = {label_id}
         GROUP BY tg.name
     """
    connection = cn.Connector()
    result = connection.execute(query)
    for row in result:
        group_spending = Class.GROUP_SPENDING(group_name=row[0],
                                              amount=float(row[1]),
                                              type="Income" if row[1] > 0 else "Expense",
                                              date=f"{datetime.today().year}/{datetime.today().month}")
        data.append(group_spending)
    return data
