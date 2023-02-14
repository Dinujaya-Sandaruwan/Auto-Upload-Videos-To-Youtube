import os
from google.oauth2.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from google.auth.credentials import Credentials
from google.oauth2.credentials import Credentials as OAuth2Credentials

key_file = "path/to/service_account_key.json"
creds = OAuth2Credentials.from_service_account_file(key_file)


SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

def upload_video(youtube, video_path, title, description, tags):
    try:
        # Create a video resource with the video file's metadata
        body=dict(
            snippet=dict(
                title=title,
                description=description,
                tags=tags,
                categoryId='22'
            ),
            status=dict(
                privacyStatus='public'
            )
        )

        # Call the API's videos.insert method to upload the video
        insert_request = youtube.videos().insert(
            part=','.join(body.keys()),
            body=body,
            media_body=video_path,
            # This parameter is optional and is only used in the API Explorer
            notifySubscribers=False
        )
        response = insert_request.execute()

        print(f'Video uploaded: https://www.youtube.com/watch?v={response["id"]}')

    except HttpError as e:
        print(f'An HTTP error {e.resp.status} occurred:\n{e.content}')

def main():
    # Replace the following values with your own:
    video_path = 'test.mp4'
    title = 'How to make a website using flask'
    description = 'Like Comment Subscribe to my channel'
    tags = ['Dinujaya', 'Website', 'Flask', 'Programming']

    # Create credentials from a service account key file
    credentials = ServiceAccountCredentials.from_json_keyfile_name('/client_secrets.json', SCOPES)

    # Build the YouTube API client
    youtube = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

    # Upload the video to YouTube
    upload_video(youtube, video_path, title, description, tags)

if __name__ == '__main__':
    main()
