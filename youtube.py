import os
from googleapiclient.discovery import build
import json
import re
from datetime import timedelta

api_key = '********************************************' ## insert your api-key here
youtube=build(serviceName='youtube',version='v3',developerKey=api_key)

## regex expression to match duration of video which is in ISO format(PL01H45M30S)
hour_pattern = re.compile(r'(\d+)H')
minute_pattern = re.compile(r'(\d+)M')
second_pattern = re.compile(r'(\d+)S')


playlist_nextPageToken=None ## holds next page token in playlist if no. of playlists are > 50(pagination)
while True:
  ## api call to get list of playlists
    request_pl = youtube.playlists().list(
        part="snippet,contentDetails",
        channelId='UC_x5XG1OV2P6uZZ5FSM9Ttw',
        maxResults=50,
        pageToken=playlist_nextPageToken
    )

    response_pl = request_pl.execute()
    playlist_ids=[]
    for item in response_pl['items']:
        playlist_ids.append(item['id'])

    for playlist_id in playlist_ids:
        videos_nextPageToken=None ## holds next page token in playlistItems if no. of videos are > 50(pagination)
        total_time=0
        while True:       
          ## api call to get list of videos
            request_plitems = youtube.playlistItems().list(
            part="id,snippet,contentDetails",
            playlistId=playlist_id,
            maxResults=50,
            pageToken=videos_nextPageToken)

            response_plitems = request_plitems.execute()

            video_ids = []
            for item in response_plitems['items']:
                video_ids.append(item['snippet']['resourceId']['videoId'])

            ## api call to get details of videos
            request_video =  youtube.videos().list(
                part="id,snippet,contentDetails",
                id=','.join(video_ids))

            response_video =request_video.execute()        

            for item in response_video['items']:

                hour = hour_pattern.search(item['contentDetails']['duration'])
                minute = minute_pattern.search(item['contentDetails']['duration'])
                second = second_pattern.search(item['contentDetails']['duration'])

                h = int(hour.group(1)) if hour else 0
                m = int(minute.group(1)) if minute else 0
                s = int(second.group(1)) if second else 0

                time = timedelta(hours = h,
                          minutes = m,
                          seconds = s).total_seconds()

                total_time+=time

            videos_nextPageToken = response_plitems.get('nextPageToken')
            if  not videos_nextPageToken:
                break
        minutes,seconds = divmod(total_time,60)
        hours,minutes = divmod(minutes,60)
        print(f'playlist_id : {playlist_id} duration : {hours}:{minutes}:{seconds}')

    playlist_nextPageToken = response_pl.get('nextPageToken')
    if not playlist_nextPageToken:
        break

