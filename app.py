import streamlit as st
from utils import load_data
from channels import display_channels_page
import plotly.express as px
from videos import display_t10_w,  display_top_each_year, distribution_cat_vid, word_cloud
import videos
import pandas as pd
st.title("Indundi Charts")
st.write("""
Welcome to the Indundi Charts! This project is aimed at providing insights and analytics on the music industry in Burundi, specifically for musicians and their fans. By analyzing data  metrics, we can help musicians understand how they are performing, identify areas for improvement, and gain insights into trends in the industry.

Through visualizations such as bar charts, scatter plots, histograms, and line plots, we can help musicians and fans better understand the data and make informed decisions about their music. Our goal is to provide a comprehensive and user-friendly platform for exploring the music industry in Burundi, with the ultimate aim of helping musicians and fans connect and thrive. So, join us as we dive into the world of Burundi music analytics!
""")

st.write("The data utilized in this project was retrieved using the YouTube Data API. It is important to note that this data may not be completely accurate, but it provides a solid foundation for further analysis and expansion in the future.")

# Define the sidebar options
SIDEBAR_OPTIONS = ["Channels", "Videos"]
df = load_data()
videos = videos.load_data()

# Create the sidebar
selection = st.sidebar.selectbox("What do you want analyze?", SIDEBAR_OPTIONS)


# Display content based on user selection
if selection == "Channels":
   display_channels_page(df)
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
    word_cloud(videos)
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


