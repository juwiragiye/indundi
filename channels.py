import pandas as pd
import streamlit as st
import plotly.express as px

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
    
