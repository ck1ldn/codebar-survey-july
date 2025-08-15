import streamlit as st
import pandas as pd
import altair as alt

csv_url = 'https://docs.google.com/spreadsheets/d/1E9mHJl7o80goyECXu631EhN3bW8OHPiNVLNr5C5JkyA/export?format=csv'

@st.cache_data
def load_data(url):
    df = pd.read_csv(url)
    # Strip trailing/leading spaces in column names
    df.columns = df.columns.str.strip()
    # Drop sensitive columns if they exist
    cols_to_hide = ['Timestamp', 'Email Address', 'full name']
    df = df.drop(columns=cols_to_hide, errors='ignore')
    return df

df = load_data(csv_url)

st.title("July PulseCheck Survey")
st.markdown("Chapter attendees by gender")

# Filter out unwanted answers
df_filtered = df[(df['What is your gender'].str.lower() != 'prefer not to say') & 
                 (df['Which chapters have you attended'].notnull())]

# Group by chapter and gender, get counts
grouped = df_filtered.groupby(['Which chapters have you attended', 'What is your gender']) \
                     .size().reset_index(name='count')

# Build stacked bar chart with Altair
chart = alt.Chart(grouped.reset_index()).mark_bar().encode(
    x=alt.X('Which chapters have you attended', sort=None, axis=alt.Axis(labels=False, title='Chapters')),
    y='count',
    color='What is your gender',
    tooltip=['Which chapters have you attended', 'What is your gender', 'count']
).properties(
    width=700,
    height=400
)



st.altair_chart(chart, use_container_width=True)


# Calculate counts and percentages
satisfaction_counts = (
    df['As a community member, how satisfied are you with codebar overall']
    .value_counts()
    .reset_index()
)
satisfaction_counts.columns = ['Satisfaction', 'Count']
satisfaction_counts['Percentage'] = (
    satisfaction_counts['Count'] / satisfaction_counts['Count'].sum() * 100
).round(1)

# Sort by percentage for nicer order
satisfaction_counts = satisfaction_counts.sort_values('Percentage', ascending=False)

# Create chart
satisfaction_chart = alt.Chart(satisfaction_counts).mark_bar().encode(
    x=alt.X('Satisfaction', sort='-y', title='Satisfaction Level'),
    y=alt.Y('Percentage', title='Percentage of Responses'),
    tooltip=['Satisfaction', 'Count', 'Percentage']
).properties(
    title='Overall Satisfaction with codebar'
)

# Display in Streamlit
st.altair_chart(satisfaction_chart, use_container_width=True)


attendance_counts = df['How many events have you attended since January 2025'] \
    .dropna() \
    .value_counts() \
    .reset_index()

attendance_counts.columns = ['Events Attended', 'Count']

chart = alt.Chart(attendance_counts).mark_bar().encode(
    x=alt.X('Events Attended', title='Number of Events Attended'),
    y=alt.Y('Count', title='Number of Participants'),
    tooltip=['Events Attended', 'Count']
).properties(
    title='Participant Event Attendance Since January 2025'
)

st.altair_chart(chart, use_container_width=True)


# Recommendation chart
recommend_counts = (
    df['How likely are you to recommend codebar to a friend or colleague?']
    .dropna()
    .value_counts()
    .reset_index()
)
recommend_counts.columns = ['Recommendation', 'Count']
recommend_counts['Percentage'] = (recommend_counts['Count'] / recommend_counts['Count'].sum() * 100).round(1)

recommend_chart = alt.Chart(recommend_counts).mark_bar().encode(
    x=alt.X('Recommendation', sort='-y', title='Likelihood to Recommend'),
    y=alt.Y('Percentage', title='Percentage of Responses'),
    tooltip=['Recommendation', 'Count', 'Percentage']
).properties(
    title='Likelihood to Recommend codebar'
)

st.altair_chart(recommend_chart, use_container_width=True)


# Filter out missing values
df_filtered = df[
    df['Which chapters have you attended'].notnull() & 
    df['How would you rate the overall quality of codebar workshops?'].notnull()
]

# Group by chapter and workshop rating
grouped = df_filtered.groupby(
    ['Which chapters have you attended', 'How would you rate the overall quality of codebar workshops?']
).size().reset_index(name='count')

# Build stacked bar chart
workshop_chart = alt.Chart(grouped).mark_bar().encode(
    x=alt.X('Which chapters have you attended', sort=None, title='Chapters'),
    y=alt.Y('count', title='Number of Responses'),
    color='How would you rate the overall quality of codebar workshops?',
     tooltip=[
        alt.Tooltip('Which chapters have you attended', title='Chapter'),
        alt.Tooltip('How would you rate the overall quality of codebar workshops?', title='Rating'),
        alt.Tooltip('count', title='Count')
    ]
).properties(
    title='Workshop Quality Ratings by Chapter',
    width=700,
    height=400
)

st.altair_chart(workshop_chart, use_container_width=True)
