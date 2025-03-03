import discogs_client
import yaml
import yt_dlp

from pydub import AudioSegment
import os

with open('configs/constants.yaml', 'r') as file:
    keys = yaml.load(file, Loader=yaml.SafeLoader)
with open('configs/run_config.yaml', 'r') as file:
    run_config = yaml.load(file, Loader=yaml.SafeLoader)
with open('configs/params_metadata.yaml', 'r') as file:
    params = yaml.load(file, Loader=yaml.SafeLoader)
with open('configs/yt_dlp.yaml', 'r') as file:
    yt_params = yaml.load(file, Loader=yaml.SafeLoader)

client = discogs_client.Client(
    'digger/0.1',
    user_token=keys['DISCOGS_KEY'])

if __name__ == '__main__':

    query_params = {key:value for key, value in run_config.items() if value is not None}
    
    if query_params['genre'] not in params['genres']:
        raise ValueError(f"Genre {query_params['genre']} not in list of genres")
    if query_params['style'] not in params['styles']:
        raise ValueError(f"Style {query_params['style']} not in list of styles")

    query_results = client.search(**query_params)

    for page_counter in range(1, query_results.pages):
        print(page_counter)
        current_page = query_results.page(page_counter)
        page_releases = len(current_page)

        for release in current_page[:1]:

            videos = release.videos
            for video in videos:
                video_url = video.url

                with yt_dlp.YoutubeDL(yt_params) as ydl:
                    ydl.download(video_url)

            for file in os.listdir('temp'):
                if file.endswith('.m4a'):
                    sound = AudioSegment.from_file(f'temp/{file}')
                    sound.export(f'temp/{file.replace(".m4a", ".wav")}', format='wav')
                    os.remove(f'temp/{file}')