from pydub import AudioSegment
import os

if __name__ == '__main__':

    local_files = 'baselines/'
    for file in os.listdir(local_files):
        curr_format = file.partition('.')[-1]
        if not file.endswith('.wav'):
            sound = AudioSegment.from_file(f'baselines/{file}')
            sound.export(f'baselines/{file.replace(curr_format, "wav")}', format='wav')
            os.remove(f'baselines/{file}')

