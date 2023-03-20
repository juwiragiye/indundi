import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import plotly.graph_objs as go
from datetime import datetime, timedelta

st.title("Indundi Charts")
st.write("""
Welcome to the Indundi Charts! This project is aimed at providing insights and analytics on the music industry in Burundi, specifically for musicians and their fans. By analyzing data  metrics, we can help musicians understand how they are performing, identify areas for improvement, and gain insights into trends in the industry.

Through visualizations such as bar charts, scatter plots, histograms, and line plots, we can help musicians and fans better understand the data and make informed decisions about their music. Our goal is to provide a comprehensive and user-friendly platform for exploring the music industry in Burundi, with the ultimate aim of helping musicians and fans connect and thrive. So, join us as we dive into the world of Burundi music analytics!
""")

st.write("The data utilized in this project was retrieved using the YouTube Data API. It is important to note that this data may not be completely accurate, but it provides a solid foundation for further analysis and expansion in the future.")

# Define the sidebar options
SIDEBAR_OPTIONS = ["Channels", "Videos"]

@st.cache_data
def load_channels():
    df = pd.read_csv("channels_data_2023-03-19.csv")
    return df

@st.cache_data
def load_videos():
    df = pd.read_csv('video_data_2023-03-19.csv')
    return df

channels = load_channels()
videos = load_videos()

# Create the sidebar
selection = st.sidebar.selectbox("What do you want analyze?", SIDEBAR_OPTIONS)

def get_top_channels_by_views(data):
    """Returns a DataFrame of the top 10 channels by view count."""
    top_channels = data.sort_values(by="view_count", ascending=False).head(10)
    return top_channels[["title", "view_count"]]
def display_top_channels_table(data):
    """Displays a table of the top 10 channels by view count."""
    top_channels = get_top_channels_by_views(data)
    top_channels = top_channels.reset_index(drop=True)
    top_channels.index += 1
    st.table(top_channels)

def get_top_channels_by_subscribers(data):
    """Returns a DataFrame of the top 10 channels by subscriber count."""
    top_channels = data.sort_values(by="subscriber_count", ascending=False).head(10)
    return top_channels[["title", "subscriber_count"]]

def display_top_channels_table_by_subs(data):
    """Displays a table of the top 10 channels by view count."""
    top_channels = get_top_channels_by_subscribers(data)
    top_channels = top_channels.reset_index(drop=True)
    top_channels.index += 1
    st.table(top_channels)

def display_channels_page(df):
    """Display channels page"""
     # Display channel content
    st.header("Burundi Music Channels Dashboard")
    st.write("""
    In this section, you will be able to explore the performance of different music channels in Burundi. You can compare the total views, subscribers, and video counts of multiple channels to gain insights into how they are performing. Additionally, you can analyze the trends in the Burundi music industry and understand what is working well for these channels.
    """)
    st.subheader("Top 10 Channels by view count")
    display_top_channels_table(df)
    st.subheader("Top 10 Channels by subscriber count")
    display_top_channels_table_by_subs(df)
    # plot the channel and views chart
    fig1 = px.bar(df.sort_values('view_count'), x='title', y='view_count',
                title='Top 10 Channels by View Count')
    st.plotly_chart(fig1)

    # plot the views and channel chart
    fig2 = px.bar(df.sort_values('subscriber_count'), x='title', y='subscriber_count',
                title='Top 10 Channels by Subscriber Count')
    st.plotly_chart(fig2)

    st.subheader('What is the average number of views per channel?')
    avg_views_per_channel = int(df['view_count'].mean())
    st.write(avg_views_per_channel)

    st.subheader('What is the average number of subscribers per channel?')
    avg_sub_per_channel = int(df['subscriber_count'].mean())
    st.write(avg_sub_per_channel)
    st.subheader('Is there a correlation between the number of subscribers and the number of views?')
    st.write("""It is evident that there is a correlation between the number of subscribers a channel has and the views it receives. Our analysis has shown that as the number of subscribers increase, so does the number of views. This suggests that having a large subscriber base is an important factor in achieving high view counts for Burundi music industry channels.
    """)
    fig3 = px.scatter(df, x="view_count", y="subscriber_count",
                 size="video_count", hover_data=['title'])

    fig3.update_layout(title="Relationship between Views and Subscribers",
                    xaxis_title="View Count",
                    yaxis_title="Subscriber Count")

    st.plotly_chart(fig3)
    st.subheader('Is there a correlation between the number of videos upload and the number of views?')
    st.write("""
    While it is true that some channels may have fewer videos but higher views, it is important to note that there is still a correlation between the number of videos uploaded and the overall view count. In general, channels that upload more frequently tend to have more views. However, there are other factors that also come into play, such as the quality of the content, the promotion strategies used, and the target audience. It is therefore essential for musicians in the Burundi music industry to find a balance between quantity and quality when creating and promoting their content.
    """)
    fig3 = px.scatter(df, x="view_count", y="video_count",
                 size="video_count", hover_data=['title'])

    fig3.update_layout(title="Relationship between Views and Number of Videos upload",
                    xaxis_title="View Count",
                    yaxis_title="Videos Uploaded")

    st.plotly_chart(fig3)
    st.subheader("Conclusion")
    st.write("From the analysis of the channels section, we can conclude that the Burundi music industry is thriving, with several channels having a substantial number of views and subscribers.")
    st.write("The top 10 channels with the highest view count all have over a million views, indicating a significant interest in Burundian music on YouTube.")
    st.write("We also observe that there is a correlation between the number of subscribers and the number of views, indicating that channels with more subscribers tend to have more views.")
    st.write("Finally, we notice that there is some variability in the relationship between the number of videos and the number of views, with some channels having more views despite having fewer videos. This suggests that while uploading more videos may increase the likelihood of getting more views, it is not a guarantee, and other factors, such as quality and popularity of the content, may also play a significant role.")
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

# def word_cloud(df):
#     tags_str = ' '.join(df['tags'])

# # Generate the word cloud
#     wordcloud = WordCloud(width=800, height=400, background_color='white').generate(tags_str)

#     # Create a dataframe of the word cloud data
#     wordcloud_df = pd.DataFrame(wordcloud.words_.items(), columns=['tag', 'count'])

#     # Sort the dataframe by count in descending order
#     wordcloud_df = wordcloud_df.sort_values(by=['count'], ascending=False)

#     # Create the Plotly bar chart
#     fig = px.bar(wordcloud_df.head(20), x='tag', y='count', color='tag', labels={'tag': 'Tag', 'count': 'Count'},
#                 title='Most Frequent Video Tags')
#     st.plotly_chart(fig)



# Display content based on user selection
if selection == "Channels":
   display_channels_page(channels)
else:
    # Display video content
    st.header("Burundi Music Charts")
    st.write("We will be analyzing the data based on various factors such as tags, published date, view count, like count, comment count, duration, and categories, which in this case are all music categories.")
    st.write("By analyzing these factors, we can gain insights into what makes a video popular, what types of music are currently trending, and how different categories are performing. ")
    st.write("This information can be used to make informed decisions about content creation and marketing strategies in the Burundi music industry.")
    st.subheader("Top Charters this week")
    display_t10_w(videos)
    st.subheader("Top Charts each year")
    display_top_each_year(videos)
    st.subheader('View Count vs Like Count for Top 100 Videos')
    # display_artists_growth(videos, df)
    # fig = px.line(videos.sort_index('view_count').head(20), x='published_at', y='view_count', color='title',
    #           title='View Count Trend over Time')
    # fig.show()
    # Get the top 100 videos by view count
    top_videos = videos.sort_values('view_count', ascending=False).head(100)

    # Create the scatter plot
    fig = px.scatter(top_videos, x='view_count', y='like_count', hover_data=['title'])

    # Add axis labels and title
    fig.update_layout(xaxis_title='View Count', yaxis_title='Like Count')

    # Show the plot
    st.plotly_chart(fig)

    st.subheader('Category and video distrubtion')
    distribution_cat_vid(videos)
    st.subheader('The most frequently used tags in the videos')
    # word_cloud(videos)
    st.subheader('Audience Engagement')
    # Create scatter plot
    fig = px.scatter(videos, x='view_count', y='like_count', color='comment_count', 
                    hover_data=['title'], title='View Count vs Like Count by Comment Count')

    # Show the plot
    st.plotly_chart(fig)

    st.subheader('Conlcusion')
    st.write('Based on the analysis of the video dataset, the following conclusions can be drawn:')
    st.write('Top Charters this week: By analyzing the top charts for this week, we can see that the top trending songs are:')
    songs = [
        '1. Drama T - ITAMPORIZE',
        '2. D-ONE - Amarira',
        '3. Vania Ice - Narahezagiwe ft B face, Dj Paulin',
        '4. Meili- KURE',
        '5. Alvin Smith - For You'
    ]
    for item in songs:
        st.write(item)

    st.write("Top charts each year: By analyzing the top charts for each year, we can identify trends in music genres and artists' popularity.")
    st.write("View Count vs Like Count for Top 100 Videos: By analyzing the view count and like count for the top 100 videos, we can see a strong correlation between the two. This indicates that videos with higher view counts also tend to have more likes, which suggests high audience engagement and satisfaction.")
    st.write("Category and video distribution: By analyzing the category and video distribution, we can see that the most popular categories are Pop Music, Hip Hop Music, and Afrobeats, and the majority of videos fall under these categories. This indicates a high demand for these types of videos, and content creators should focus on creating videos in these categories to attract more viewers.")
    st.write("""The most frequently used tags in the videos: By analyzing the most frequently used tags in the videos, we can identify the topics that are popular among viewers. This information can be used to create targeted content and increase the chances of videos being discovered by interested viewers. We can also see that most artists don't use good tags for their songs. This means artits should add relevant tags to the videos to target their audience.""")
    st.write('Audience Engagement: By analyzing the engagement rate of the videos, we can identify the most engaging videos and the factors that contribute to high audience engagement. This information can be used to create more engaging content and increase the likelihood of viewers watching the entire video and interacting with it.')
    st.write('Overall, the analysis of the dataset provides valuable insights into the music industry and can be used to inform content creation, marketing, and promotion strategies for artists and content creators.')
    st.subheader("If you have any feedback, questions or suggestions for how to improve this project, please don't hesitate to reach out to me on Twitter! My handle is @janvitech.")


