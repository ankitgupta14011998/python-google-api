import os
from googleapiclient.discovery import build
import json
import re
from datetime import timedelta

api_key = '*********************************************' ## put your api key here
youtube=build(serviceName='youtube',version='v3',developerKey=api_key)


nextPageToken = None
videolist=[]
while True:
    request_plitems = youtube.playlistItems().list(
        part="id,snippet,contentDetails",
        playlistId='PLc2EZr8W2QIBegSYp4dEIMrfLj_cCJgYA',
        maxResults=50,
        pageToken=nextPageToken
    )
    response_plitems = request_plitems.execute()
    video_ids = []
    for item in response_plitems['items']:
        video_ids.append(item['snippet']['resourceId']['videoId'])
    
    request_video =  youtube.videos().list(
        part="id,snippet,contentDetails,statistics",
        id=','.join(video_ids))
    
    response_video =request_video.execute()        
    
    for item in response_video['items']:
        videolist.append({'video_title' : item['snippet']['title'], 'Views': int(item['statistics']['viewCount'])})
    
    nextPageToken=response_plitems.get('nextPageToken')
    if not nextPageToken:
        break
videolist.sort(key= lambda x: x['Views'],reverse=True)
for item in videolist:
    print(item)
