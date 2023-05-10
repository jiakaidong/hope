# -*- coding: utf-8 -*-
"""final.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1tuSezwvJbb7sgCGIrg6oSKslK_Q2-E6t

**STEP 1**: The notebook shall connect to the ecsel_database.db and extract the list of countries in a dataframe.
"""

import sqlite3
import pandas as pd
import streamlit as st

# Create a connection to the SQLite database file
conn = sqlite3.connect('ecsel_database.db')

# Query the database to extract the list of countries
df_countries = pd.read_sql_query("SELECT * FROM table1", conn)

# Close the database connection
conn.close()

# Display the dataframe
print(df_countries)

"""# Nueva sección

**STEP 2**: The system shall ask the user to input a country acronym, through a dropdown menu (or directly ask the user to input a country acronym, and validate within the country list in the final.ipynb notebook)The system shall get the country acronym from the given dictionary.
"""

# Create a connection to the SQLite database file
conn = sqlite3.connect('ecsel_database.db')

# Read the data from the 'table1' table
df = pd.read_sql_query("SELECT * from table1", conn)

# Close the database connection
conn.close()

# Get the list of country acronyms
country_acronyms = df['Acronym'].tolist()

# Ask the user to input a country acronym
country_acronym = input("Please enter a country acronym: ")

# Validate the input
if country_acronym not in country_acronyms:
    print("Invalid input. Please enter a valid country acronym.")
else:
    print("Valid input.")

"""**STEP 3**: The system shall get the country acronym from the given country_acronyms dictionary.

**STEP 4**: The system shall connect to the database and generate a new dataframe of participants (from the organizations table in the database). It will contain the total amount of received grants per partner
in the selected country ( =SUM(ecContribution) ) . It should include the following fields: shortName, name , activityType (Research institution, Private company, ...), organizationURL (web page), SUM(ecContribution).
"""

# Connect to the SQLite database
conn = sqlite3.connect('ecsel_database.db')

# Define the SELECT query to retrieve the data from the organizations table for the selected country
query = f"""SELECT shortName, name, activityType, organizationURL, SUM(ecContribution) as total_grants
            FROM table2
            WHERE country='{selected_country}'
            GROUP BY shortName"""

# Execute the query and store the results in a pandas dataframe
df_participants = pd.read_sql_query(query, conn)

# Print the dataframe to check the results
print(df_participants)

"""**STEP 5:** The system shall display the generated dataset, in descending order by received grants."""

df_participants = df_participants.sort_values('total_grants', ascending=False)

# Print the dataframe to check the results
print(df_participants)

"""**STEP 6**: The system shall connect to the database and generate a new project dataframe with the project coordinators from the selected country (from the organizations table in the database). This dataset should filter only project coordinators and include the following fields: shortName, name, activityType, projectAcronym."""

# Define the SELECT query to retrieve the data from the organizations table for the selected country
query = f"""SELECT shortName, name, activityType, projectAcronym
            FROM table2
            WHERE country='{selected_country}' AND role='coordinator'"""

# Execute the query and store the results in a pandas dataframe
df_projects = pd.read_sql_query(query, conn)

# Print the dataframe to check the results
print(df_projects)

"""**STEP 7**: The system shall display the generated coordinator dataset, in ascending order by shortName."""

# Sort the dataframe by shortName in ascending order
df_coordinators = df_projects.sort_values('shortName', ascending=True)

# Print the dataframe to check the results
print(df_coordinators)

"""**STEP 8**: The system shall save the generated datasets (participants, and project coordinators) in an CSV file. (There should be 2 buttons to download data)."""

# Save the participants dataframe as a CSV file
df_participants.to_csv('participants.csv', index=False)

# Save the coordinators dataframe as a CSV file
df_coordinators.to_csv('coordinators.csv', index=False)

import ipywidgets as widgets
from IPython.display import FileLink

# Create the participants download button
participants_button = widgets.Button(description='Download participants')
participants_link = FileLink('participants.csv', result_html_prefix="Click here to download: ")
display(participants_button, participants_link)

# Create the coordinators download button
coordinators_button = widgets.Button(description='Download coordinators')
coordinators_link = FileLink('coordinators.csv', result_html_prefix="Click here to download: ")
display(coordinators_button, coordinators_link)