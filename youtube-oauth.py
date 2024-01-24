import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request ## to make web requests from oauth client

credentials = None
scopes = ['https://www.googleapis.com/auth/youtube.readonly'] ## define scope, what part of users information appl need

if os.path.exists('token.pickle'): ## check if token credentials file exists, if yes then extract the creds
    print("Loading credentials from file...")
    with open('token.pickle','rb') as token:
        credentials = pickle.load(token)

if not credentials or not credentials.valid: ## if credentials doesn't exist or not a valid credentials(access_token expired or refresh token expired)
    if credentials and credentials.expired and credentials.refresh_token: ## if credentials present but acces_token_expired(refresh token exists)
        print("Refreshing the access tokens...")
        credentials.refresh(Request())
    else: ## if refresh token also expired then request for new creds and save it token.pickle file
        print("Fetching new Tokens...")
        flow = InstalledAppFlow.from_client_secrets_file("client_secrets.json",scopes=scopes)
        flow.run_local_server(port=8080,prompt="consent",authorization_prompt_message="")
        credentials= flow.credentials

        with open('token.pickle','wb') as token:
            print("Saving crdentials for future use...")
            pickle.dump(credentials,token)

youtube = build(serviceName='youtube',version='v3',credentials=credentials) ## make api call to youtube data api

request = youtube.playlistItems().list(part = 'contentDetails,snippet',playlistId='PLjItWrC65JyVhrl3NUVUnFt0awFHMRnDw') ## gather playlistItems details

response = request.execute()
print(response)
