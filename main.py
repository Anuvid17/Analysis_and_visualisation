from googleapiclient.discovery import build
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Setting up the API key and channel_id
api_key = "AIzaSyDccv7QVLZ5_I6VpLPemFnLwwCI49KEr8k"
channel_id = ["UC1pfsmDBnMQB8sOuQvmTvRQ",
              "UCMY7ZvLB6-DnuSis_2s37_A",
              "UC7Q0EfPzTwtanMVSWuK_QXA",
              "UCzw4hbQIePVtyJQzE_F8QDg",
              "UCZ50rYSkYQG31YDEJm9Di_g",
              "UCcErZD9wUPQONYaoRXWX-hw",
              "UC24sjKTMy-d5Z-g2OsYYHqw"]

# Creating the youtube service
youtube = build('youtube', 'v3', developerKey=api_key)

# Creating function to extract the channel details
def get_channel(youtube, channel_id):
    all_data = []
    request = youtube.channels().list(
        part = 'snippet,contentDetails,statistics',
        id=','.join(channel_id))
    response = request.execute()

    for i in range(len(response['items'])):
      data = dict(Channel_name = response['items'] [i] ['snippet'] ['title'],
                  Subscribers = response['items'] [i] ['statistics'] ['subscriberCount'],
                  Views = response['items'] [i] ['statistics'] ['viewCount'],
                  Videos = response['items'] [i] ['statistics'] ['videoCount'])
      
      all_data.append(data)
    return all_data

# For Tableau Format
channel_statistics = get_channel(youtube, channel_id)
channel_data = pd.DataFrame(channel_statistics)

# Converting string into integer datatype
channel_data['Subscribers'] = pd.to_numeric(channel_data['Subscribers'])
channel_data['Views'] = pd.to_numeric(channel_data['Views'])
channel_data['Videos'] = pd.to_numeric(channel_data['Videos'])
channel_data.dtypes
print(channel_data)

# For Visualisation
sns.set(rc = {'figure.figsize':(10,8)})
ax = sns.barplot(x = 'Channel_name', y = 'Subscribers', data = channel_data)
plt.xticks(rotation=45)  # Rotate x-axis labels for better readability
plt.tight_layout()  # Adjust layout to prevent label cutoff
plt.show()  # Show the plot
