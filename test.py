#!/usr/bin/python

import httplib2
import os
import random
import sys
import time

from apiclient.discovery import build
from apiclient.errors import HttpError
from apiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

httplib2.RETRIES = 1

MAX_RETRIES = 10

RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error)

RETRIABLE_STATUS_CODES = [500, 502, 503, 504]

CLIENT_SECRETS_FILE = "client_secrets.json"

YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

%s

with information from the API Console
https://console.cloud.google.com/

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(file), CLIENT_SECRETS_FILE))

VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")


def get_authenticated_service(args):


flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
                               scope=YOUTUBE_UPLOAD_SCOPE,
                               message=MISSING_CLIENT_SECRETS_MESSAGE)

storage = Storage("%s-oauth2.json" % sys.argv[0])
credentials = storage.get()

if credentials is None or credentials.invalid:
credentials = run_flow(flow, storage, args)

return build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
             http=credentials.authorize(httplib2.Http()))


def initialize_upload(youtube, options):


body = dict(
    snippet=dict(
        title="Dinujaya Sandaruwan",
        description="Like comment Subscribe",
        tags=["Saman", "Kumara"],
    ),
    status=dict(
        privacyStatus="public",
    )
)

insert_request = youtube.videos().insert(
    part=",".join(body.keys()),
    body=body,
    media_body=MediaFileUpload(options.file, chunksize=-1, resumable=True)
)

resumable_upload(insert_request)


def resumable_upload(insert_request):


response = None
error = None
retry = 0
while response is None:
try:
status, response = insert_request.next_chunk()
if response is not None:
if 'id' in response:
print("Video id '%s' was successfully uploaded.", response['id'])
else:
exit("The upload failed with an unexpected response: %s", response)
except HttpError as e:
if e.resp.status in RETRIABLE_STATUS_CODES:
error = e
if retry > MAX_RETRIES:
exit("No longer attempting to retry.")
sleeptime = random.random() * (2**retry)
print("Sleeping %f seconds and then retrying...", sleeptime)
time.sleep(sleeptime)
retry += 1
else:
exit("HTTP Error: %s", e)
