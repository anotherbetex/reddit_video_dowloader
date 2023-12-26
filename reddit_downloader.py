import os
from urllib import request
import ffmpeg
import requests
import urllib.request
import re

url = input('URL: ')

if url[-1] == '/':
    url = url[:-1]

url_json = url + '.json'
file_name = url.split("/")[-2] + '.mp4' if url[-1] == '/' else url.split("/")[-1] + '.mp4'
#file_name = url.split("/")[-2] if url[-1] == '/' else url.split("/")[-1]

headers = {
    'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36"}

data = requests.get(url_json, headers=headers).json()

fallback_video = data[0]['data']['children'][0]['data']['secure_media']['reddit_video']['fallback_url']
print(fallback_video)
fallback_audio = re.sub('DASH_(480|720|1080)', 'DASH_AUDIO_128', fallback_video)
print(fallback_audio)
print('Downloading Video...')
urllib.request.urlretrieve(fallback_video, filename='reddit_video.mp4')
print('Video Downloaded.')

try:
    urllib.request.urlretrieve(fallback_audio, filename='reddit_audio.mp4')
    audio = True

except Exception as err:
    audio = False
    print(f'No Audio')

input_video = ffmpeg.input('reddit_video.mp4')

if audio:
    print('converting...')
    input_audio = ffmpeg.input('reddit_audio.mp4')
    print('converted.')
    ffmpeg.concat(input_video, input_audio, v=1, a=1).output(f'{file_name}') \
        .global_args('-y').run(quiet=True)

    print('Removing old files...')
    os.remove('reddit_audio.mp4')
    os.remove('reddit_video.mp4')
    print('Files removed.')

else:
    print('converting...')
    ffmpeg.concat(input_video).output(f'{file_name}').global_args('-y').run(quiet=True)
    print('converted.')


    print('Removing old files...')
    os.remove('reddit_video.mp4')
    print('Files removed.')

print('Done')
