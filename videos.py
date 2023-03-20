import pandas as pd
from datetime import datetime, timedelta
import streamlit as st
import plotly.express as px
import plotly.graph_objs as go
from wordcloud import WordCloud
import matplotlib.pyplot as plt


@st.cache_data
def load_data():
    df = pd.read_csv('video_data_2023-03-19.csv')
    return df



def get_10_trending_weekly(df):
    """
    Get the 10 most trending weekly songs
    """
    now = datetime.utcnow()
    start_of_month = pd.to_datetime(datetime(now.year, now.month, 1), utc=True)
    end_of_month = pd.to_datetime(start_of_month + timedelta(days=31), utc=True)

    # Filter the dataset to include only videos published this month
    df['published_at'] = pd.to_datetime(df['published_at'])

    mask = (df['published_at'] >= start_of_month) & (df['published_at'] < end_of_month)
    print(mask)
    df_month = df.loc[mask]

    # Calculate a weighted score for each video based on views, likes, and comments
    df_month['score'] = df_month['view_count'] + df_month['like_count'] + df_month['comment_count']

    # Sort the dataset by score in descending order and get the top 10 videos
    top_10 = df_month.sort_values('score', ascending=False).head(10)
    top = pd.DataFrame()
    top['Title'] = top_10['title']
    top['Number of views'] = top_10['view_count']
    top['Number of likes'] = top_10['like_count']
    top['Number of comments'] = top_10['comment_count']
    return top


def display_t10_w(df: pd.DataFrame):
    """
    Display the 10 most trending weekly songs
    """
    top_10 = get_10_trending_weekly(df)
    top_10 = top_10.reset_index(drop=True)
    top_10.index += 1
    st.table(top_10)

def display_top_chartes_year(df: pd.DataFrame):
    # Filter to rows from this year
    this_year = df[df['published_at'].dt.year == 2023]

    # Create a new column that sums the view, comment, and like counts
    this_year['total_engagement'] = this_year['view_count'] + this_year['comment_count'] + this_year['like_count']

    # Sort the DataFrame based on the total_engagement column
    sorted_df = this_year.sort_values(by='total_engagement', ascending=False).head(10)

    # Select the top charters
    top = pd.DataFrame()
    top['Title'] = sorted_df['title']
    top['Number of views'] = sorted_df['view_count']
    top['Number of likes'] = sorted_df['like_count']
    top['Number of comments'] = sorted_df['comment_count']
    top = top.reset_index(drop=True)
    top.index += 1
    st.table(top)

def display_top_each_year(df):
    # Create a dropdown menu for selecting a year
    year = st.selectbox('Select a year:', df['published_at'].dt.year.unique())

    # Filter the data for the selected year
    filtered_df = df[df['published_at'].dt.year == year]

    # Sort the data by views, likes, and comments in descending order
    sorted_df = filtered_df.sort_values(by=['view_count', 'like_count', 'comment_count'], ascending=False).head(10)

    # Display the top 10 trending songs for the selected year
    
    top = pd.DataFrame()
    top['Title'] = sorted_df['title']
    top['Number of views'] = sorted_df['view_count']
    top['Number of likes'] = sorted_df['like_count']
    top['Number of comments'] = sorted_df['comment_count']
    top = top.reset_index(drop=True)
    top.index += 1
    st.dataframe(top)

# def display_artists_growth(df_videos: pd.DataFrame, df_channels: pd.DataFrame):
#     channels_dataframe = df_channels.rename(columns={'title': 'channel_title'})
#     df = pd.merge(df_videos, channels_dataframe[['channel_id', 'channel_title']], on='channel_id', how='left')
#     # st.table(df)
#     channel_titles = df['channel_title'].unique().tolist()
#     selected_channel = st.selectbox('Select Channel', channel_titles)

    
#     filtered_df = df[df['channel_title'] == selected_channel]

#     # Sort data by published_at
#     filtered_df = filtered_df.sort_values(by='published_at')
#     st.dataframe(filtered_df)
    
# def display_top_growth_rate(df):
#     growth_rate = df.copy()
#     growth_rate['growth_rate'] = df.groupby('channel_id')['view_count'].pct_change()

#     # Sort the values in descending order and get the top 10
#     top_10 = growth_rate.groupby('title')['growth_rate'].last().sort_values(ascending=False).head(10)
#     st.dataframe(top_10)

def distribution_cat_vid(df):
    # Create a new dataframe with the count of videos in each category
    # Split categories into a list and count the number of videos in each category
    # create a list of all categories
    df['category'] = df['categories'].explode()

# Count the frequency of each category
    category_counts = df['category'].value_counts().head(5)
    # create a bar chart
    fig = go.Figure(data=[go.Bar(x=category_counts.index, y=category_counts.values)])

    # set the title and axis labels
    fig.update_layout(title='Video Categories', xaxis_title='Category', yaxis_title='Number of Videos')

    # Show the chart    
    st.plotly_chart(fig)

def word_cloud(df):
    tags_str = ' '.join(df['tags'])

# Generate the word cloud
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(tags_str)

    # Create a dataframe of the word cloud data
    wordcloud_df = pd.DataFrame(wordcloud.words_.items(), columns=['tag', 'count'])

    # Sort the dataframe by count in descending order
    wordcloud_df = wordcloud_df.sort_values(by=['count'], ascending=False)

    # Create the Plotly bar chart
    fig = px.bar(wordcloud_df.head(20), x='tag', y='count', color='tag', labels={'tag': 'Tag', 'count': 'Count'},
                title='Most Frequent Video Tags')
    st.plotly_chart(fig)


