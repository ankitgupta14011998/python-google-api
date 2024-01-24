# python-google-api

### youtube-playlist-duration

Simple python code that used developerKey from google-api and then access youtube data api resource to get duration of all the playlist in a youtube channel.

### youtube-playlist-video-sort

Python code to sort the videos in a playlist based on popularity(views)

### youtube-api-OAUTH 2.0

To make api calls to youtube service by using google's oauth 2.0 method

1. create OAUTH 2.0 application in google developer console, provide app name, developer email_id, request_uri(redirect url after authorisation - I have given localhost:8080 in my case)
2. the client_secrets.json file is generated which contains client_id and client_secret_key. This can be used to make requests from application to google to authenticate the app and get the users consent.
3. using flow.InstalledAppFlow to provide client_Secrets and scope of service that we need information from user.
4. run the local_server using flow.run_local_server which will be used for authentication(we can provide provide our website here).
5. save the creds in token.pickle file. now the connection is established, this can be used to make api calls.
