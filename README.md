
# Financial Analysis API

This project is a FastAPI-based RESTful API for managing and analyzing financial transactions. It provides endpoints to track expenses, income, and various categorizations of spending over time.

## Table of Contents
- [Features](#features)
- [Technologies](#technologies)
- [API Endpoints](#api-endpoints)

## Features

1. User Authentication
   - Description: The API uses HTTP Basic Authentication to verify user identities before granting access to their data. This adds a layer of security, ensuring that only authorized users can view or manipulate their financial records.
   - Benefits: Enhances data security and privacy by ensuring sensitive information is only accessible to rightful users.

2. Load and Analyze Monthly Spending and Income Data
   - Description: The API allows users to load their monthly income and expense data from the database, providing insights into their financial habits.
   - Benefits: Users can track their financial health over time, identify spending patterns, and make more informed financial decisions.

3. Spending Analysis Over Defined Ranges
   - Description: Users can analyze their spending trends over specific timeframes, comparing their actual spending against expected norms or budgets.
   - Benefits: This feature helps users to monitor their budgeting effectiveness and adjust spending behavior accordingly to avoid overspending.

4. Breakdown of Spending by Transaction Groups
   - Description: The API allows users to categorize their spending by different groups such as groceries, entertainment, or bills, which can be adjusted in the database.
   - Benefits: This granularity in transaction categorization helps users understand where their money is going and identify areas for potential savings.

5. Categorization via Labels
   - Description: Spending can be further categorized using labels, offering additional insights beyond transaction groupings.
   - Benefits: Provides users with customizable and detailed reports on specific areas of spending, allowing for better management of their finances.

6. Trend Analysis for Income and Expenses
   - Description: Users can analyze trends in their income and expenses over defined date ranges, allowing them to assess changes in their financial situation over time.
   - Benefits: Identifies patterns that can signify financial health issues or improvements, helping users proactively manage their finances.

7. Detailed Transaction History
   - Description: The API maintains a comprehensive history of transactions, including details about the amount, date, labels, and group classifications.
   - Benefits: Users can review their complete transaction history for better insight and tracking of their financial activities.

8. Flexible Reporting
   - Description: Users can request reports based on various parameters, including specific time periods or specific labels/groups.
   - Benefits: This flexibility in reporting allows users to customize their insights according to their needs and preferences.

9. Real-time Data Access
   - Description: The API processes requests in real-time, allowing users instantaneous access to their data.
   - Benefits: Users can make timely financial decisions based on their most current data without delays.

10. CORS and HTTPS Support
    - Description: The API is configured to allow cross-origin resource sharing (CORS) to enable secure access from web applications and enforce HTTPS for secure data transmission.
    - Benefits: Enhances security and fosters usability across different platforms and devices while protecting user data in transit.

11. Cache Control
    - Description: Responses are cached to improve performance and reduce server load through appropriate cache control headers.
    - Benefits: Speeds up response times for frequently requested data, providing a smoother user experience.

12. Comprehensive Data Validation
    - Description: The API incorporates data validation through Pydantic, ensuring that the incoming data adheres to the expected format.
    - Benefits: Reduces the likelihood of data corruption and enables better error handling, ensuring the integrity of the data being processed.

## Technologies
- [FastAPI](https://fastapi.tiangolo.com/) - The web framework used for building the API
- [SQLAlchemy](https://www.sqlalchemy.org/) - ORM for database interaction
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation and settings management using Python type annotations
- [MySQL](https://www.mysql.com/) - Database for storing user and transaction data
- [Python](https://www.python.org/) - Programming language used for the project

##API Endpoints
- GET /: Root endpoint that returns a welcome message.
- GET /users/me: Retrieves the current user's information based on provided credentials.
- GET /spending/analysis: Analyzes the user's spending and returns expected spending metrics.
- GET /spending/income-expense/in-range: Gets income and expense data for specified date ranges.
- GET /spending/transection-group/in-month/: Provides a breakdown of spending by group for a specified month.
- GET /spending/transaction-group/in-range: Reports transaction groups over a range of months.
- GET /spending/lable/in-range: Retrieves label-based spending data over a specified date range.
- GET /spending/label/in-transaction-group: Returns spending breakdown based on labels.


   
