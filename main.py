import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import pytube
from random_word import RandomWords
import google.auth
from googleapiclient.discovery import build
from youtube_upload.client import YoutubeUploader

r = RandomWords()

# Set up the OAuth2 client
scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]
flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
"client_secret.json", scopes=scopes
)
credentials = flow.run_local_server(port=8080)

# Set up the YouTube API client
youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

# Search for videos
keyword = r.get_random_word()
request = youtube.search().list(
    part="id,snippet",
    q=keyword,
    type="video",
    maxResults=2,
    videoDefinition="high",
    videoLicense="creativeCommon",
)
response = request.execute()

for item in response["items"]:

    # DOWNLOAD VIDEOS

    video_id = item["id"]["videoId"]
    video = pytube.YouTube(f"https://www.youtube.com/watch?v={video_id}")
    print(f"https://www.youtube.com/watch?v={video_id}")
    stream = video.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc().first()
    if stream.resolution == '720p':
        stream.download(output_path=os.path.abspath("videos"), filename=f"video.mp4")
        print(f"Downloaded {video.title} in 720p resolution")
    else:
        max_res_stream = video.streams.filter(file_extension='mp4').order_by('resolution').desc().first()
        max_res_stream.download(output_path=os.path.abspath("videos"), filename=f"video.mp4")
        print(f"Downloaded {video.title} in maximum available resolution")


    # GET INFORMATIONS
    
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
    # video_title = video_response["items"][0]["snippet"]["title"]
    # video_desc = video_response["items"][0]["snippet"]["description"]
    # video_tags = video_response["items"][0]["snippet"]["tags"]
    # video_thumbnail = video_response["items"][0]["snippet"]["thumbnails"]["high"]["url"]
    video_title = "Dinujaya Sandaruwan"
    video_desc = "Dinujaya Sandaruwan"
    video_tags =[]
    # video_thumbnail = "Dinujaya Sandaruwan"





    # UPLOAD TO THE YOUTUBE

    client_id = "80299086960-7s0vkuefkcd77cur1kf7nj7j4b2ikm5g.apps.googleusercontent.com"
    client_secret = "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"



    # Video options
    options = {
        "title" : video_title, # The video title
        "description" : video_desc, # The video description
        "tags" : video_tags,
        "categoryId" : "22",
        "privacyStatus" : "unlisted", # Video privacy. Can either be "public", "private", or "unlisted"
        # "thumbnail_path" : video_thumbnail, # Path to the thumbnail image file
        "kids" : False, # Specifies if the Video if for kids or not. Defaults to False.
    }

    # upload video
    def upload_video(video):
        uploader = YoutubeUploader(client_id,client_secret)
        uploader.authenticate(oauth_path='oauth.json')
        uploader.upload(video, options) 
        print("successfully uploaded video to youtube! ❤️")
        
        uploader.close()

    upload_video("videos/video.mp4")

    