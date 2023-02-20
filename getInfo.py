import google.auth
from googleapiclient.discovery import build

# User inputs the YouTube video URL
video_url = input("Enter the YouTube video URL: ")

# Extract the video ID from the URL
video_id = video_url.split("=")[-1]

# Set the API key
api_key = "AIzaSyDX76Sk7nnMbEh9zXYumt-Q8_qhPXpbIFQ"

# Authenticate the API request using the API key
youtube = build("youtube", "v3", developerKey=api_key)

# Call the API to get the video details
video_response = youtube.videos().list(
    part="snippet",
    id=video_id
).execute()

# Extract the title, description, tags, and thumbnail URL from the video response
video_title = video_response["items"][0]["snippet"]["title"]
video_desc = video_response["items"][0]["snippet"]["description"]
video_tags = video_response["items"][0]["snippet"]["tags"]
video_thumbnail = video_response["items"][0]["snippet"]["thumbnails"]["high"]["url"]

# Print the video details
print("Video Title: ", video_title)
print("Video Description: ", video_desc)
print("Video Tags: ", video_tags)
print("Video Thumbnail URL: ", video_thumbnail)
