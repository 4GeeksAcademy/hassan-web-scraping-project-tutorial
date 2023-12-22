import requests
import time
from bs4 import BeautifulSoup
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3

# URL of the page to scrape
url = "https://api.scrapingdog.com/scrape?api_key=657d045fa8510675fba81d9e&url=https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue&dynamic=false"


# Sending a request to the website
response = requests.get(url)
print(response.status_code)

# Parse the HTML snippet
soup = BeautifulSoup(response.text, 'html.parser')

tables = soup.find_all('table', class_='historical_data_table')
quarterly_revenue_table = None
for table in tables:
    if "Quarterly Revenue" in table.text:
        quarterly_revenue_table = table
        break

# Check if the table was found
if not quarterly_revenue_table:
    print("Quarterly Revenue table not found")
else:
    # Initialize a list to store the quarterly revenue data
    quarterly_revenue_data = []

    # Iterate over each row in the table body
    for row in quarterly_revenue_table.tbody.find_all('tr'):
        # Extract the date and revenue from each cell
        date_td, revenue_td = row.find_all('td')
        date = date_td.text.strip()
        revenue = revenue_td.text.strip()

        # Append the extracted data to the list
        quarterly_revenue_data.append({'date': date, 'revenue': revenue})

    # Display the extracted data
    for data in quarterly_revenue_data:
        print(f"Date: {data['date']}, Revenue: {data['revenue']}")


# Create a DataFrame
df = pd.DataFrame(quarterly_revenue_data)

# Display the DataFrame
print(df)

# If you want to save this DataFrame to a CSV file
df.to_csv('quarterly_revenue_data.csv', index=False)


df = df[df["revenue"] != ""]
df.head()


conn = sqlite3.connect('my_database.db')
conn


# Create a cursor object using the cursor() method
cursor = conn.cursor()

# Drop the table if it already exists
cursor.execute("""CREATE TABLE df (Date, Revenue)""")

tesla_tuples = list(df.to_records(index = False))
tesla_tuples[:5]

cursor.executemany("INSERT INTO df VALUES (?,?)", tesla_tuples)
conn.commit()

for row in cursor.execute("SELECT * FROM df"):
    print(row)


fig, axis = plt.subplots(figsize = (10, 5))

df["date"] = pd.to_datetime(df["date"])
df["revenue"] = df["revenue"].astype('int')
sns.lineplot(data = df, x = "date", y = "revenue")

plt.tight_layout()

plt.show()


fig, axis = plt.subplots(figsize = (10, 5))

df["date"] = pd.to_datetime(df["date"])
tesla_revenue_yearly = df.groupby(df["date"].dt.year).sum().reset_index()

sns.barplot(data = tesla_revenue_yearly[tesla_revenue_yearly["date"] < 2023], x = "date", y = "revenue")

plt.tight_layout()

plt.show()


fig, axis = plt.subplots(figsize = (10, 5))

tesla_revenue_monthly = df.groupby(df["date"].dt.month).sum().reset_index()

sns.barplot(data = tesla_revenue_monthly, x = "date", y = "revenue")

plt.tight_layout()

plt.show()