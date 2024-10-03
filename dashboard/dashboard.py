import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
sns.set(style='dark')

# Load the datasets
day_df = pd.read_csv('data/day.csv')
hour_df = pd.read_csv('data/hour.csv')

# Convert the 'dteday' column to datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

st.sidebar.title("Filter Data")
start_date = st.sidebar.date_input("Start Date", day_df['dteday'].min())
end_date = st.sidebar.date_input("End Date", day_df['dteday'].max())

# Filter the data based on the selected dates
day_filtered = day_df[(day_df['dteday'] >= pd.to_datetime(start_date)) & 
                      (day_df['dteday'] <= pd.to_datetime(end_date))]
hour_filtered = hour_df[(hour_df['dteday'] >= pd.to_datetime(start_date)) & 
                        (hour_df['dteday'] <= pd.to_datetime(end_date))]
st.title("Bike Sharing Data Dashboard")
st.markdown("""
This dashboard provides insights into bike rentals based on weather, time of day, and other factors.
Use the date filter in the sidebar to select a date range for analysis.
""")

st.subheader("Filtered Data Overview")
st.write(day_filtered.head())

# Average Bike Rentals by Hour of the Day
st.subheader('Average Bike Rentals by Hour of the Day')
hourly_rentals = hour_df.groupby('hr')['cnt'].mean()
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(hourly_rentals.index, hourly_rentals.values, marker='o', color='orange')
ax.set_title('Average Bike Rentals by Hour of the Day')
ax.set_xlabel('Hour of the Day')
ax.set_ylabel('Average Rentals')
st.pyplot(fig)

hour_df['weathersit'] = hour_df['weathersit'].map({
    1: 'Clear',        # 1 means Clear weather
    2: 'Cloudy',       # 2 means Cloudy weather
    3: 'Bad Weather'   # 3 means Bad Weather
}) 

# Define the function to categorize time into Morning, Afternoon, and Evening
def categorize_time_of_day(hour):
    if 6 <= hour < 12:
        return 'Morning'
    elif 12 <= hour < 18:
        return 'Afternoon'
    else:
        return 'Evening'

# Create the 'time_of_day' column in the DataFrame
hour_df['time_of_day'] = hour_df['hr'].apply(categorize_time_of_day)

# Group by 'time_of_day' and 'weathersit', then calculate the mean number of rentals (cnt)
cluster_counts = hour_df.groupby(['time_of_day', 'weathersit']).agg({'cnt': 'mean'}).reset_index()

# Plotting the results
fig2, ax2 = plt.subplots(figsize=(10, 5))
sns.barplot(x='time_of_day', y='cnt', hue='weathersit', data=cluster_counts, ax=ax2, palette="Blues")
ax2.set_title('Average Bike Rentals by Time of Day and Weather Condition')
ax2.set_xlabel('Time of Day')
ax2.set_ylabel('Average Rentals')

# Display the plot in Streamlit
st.pyplot(fig2)


# Group the data by weather condition
weather_grouped = day_filtered.groupby('weathersit').agg({'cnt': 'mean'}).reset_index()

# Plot
fig, ax = plt.subplots()
sns.barplot(x='weathersit', y='cnt', data=weather_grouped, palette='Blues', ax=ax)
ax.set_title('Average Rentals by Weather Condition')
ax.set_xlabel('Weather Condition')
ax.set_ylabel('Average Bike Rentals')

st.pyplot(fig)

# Create a column for time of day
def time_of_day(hour):
    if 5 <= hour < 12:
        return "Morning"
    elif 12 <= hour < 18:
        return "Afternoon"
    else:
        return "Evening"

hour_filtered['time_of_day'] = hour_filtered['hr'].apply(time_of_day)

# Group data by time of day
time_weather_grouped = hour_filtered.groupby(['time_of_day', 'weathersit']).agg({'cnt': 'mean'}).reset_index()

# Plot
fig, ax = plt.subplots()
sns.barplot(x='time_of_day', y='cnt', hue='weathersit', data=time_weather_grouped, palette='Blues', ax=ax)
ax.set_title('Average Bike Rentals by Time of Day and Weather')
ax.set_xlabel('Time of Day')
ax.set_ylabel('Average Bike Rentals')

st.pyplot(fig)

st.subheader("Key Metrics")

total_rentals = day_filtered['cnt'].sum()
avg_rentals = day_filtered['cnt'].mean()

col1, col2 = st.columns(2)
col1.metric("Total Rentals", f"{total_rentals}")
col2.metric("Average Rentals", f"{avg_rentals:.2f}")

