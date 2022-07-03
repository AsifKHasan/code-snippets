#!/usr/bin/env python3

import sys
import json
import codecs
import argparse
import requests
from pydub import AudioSegment
from pydub.silence import split_on_silence

def get_text_from_audio(audio_file_path, reference_text=None):
    request_json = {
        'files': open(audio_file_path, 'rb')
    }

    response = requests.post(
        "https://nlp.celloscope.net/nlp/dataset/v1/audio/speech-to-text",
        data={'referenceText' : reference_text},
        files=request_json
    )

    json_response = json.loads(response.text)
    return json_response



MAX_AUDIO_SECONDS_ALLOWED = 40
MIN_AUDIO_SECONDS_ALLOWED = 5

input_wav_file = "C:/Users/Asif Hasan/Downloads/audio/somoy-tv.wav"
output_file_format = "C:/Users/Asif Hasan/Downloads/audio/splits/somoy-tv-{}.wav"

#reading from audio mp3 file
sound = AudioSegment.from_wav(input_wav_file)

print(f"audio file    : {input_wav_file}")
print(f"duration (s)  : {sound.duration_seconds:6.2f}")
print(f"channels      : {sound.channels}")
print(f"loudness      : {sound.dBFS} dBFS")
print(f"sample width  : {sound.sample_width} byte(s)")
print(f"frame rate    : {sound.frame_rate}")
print(f"max amplitude : {sound.max}")
print(f"max loudness  : {sound.max_dBFS}")
print('\n')


# spliting audio files
audio_chunks = split_on_silence(sound, min_silence_len=1000, silence_thresh=-40 )


# loop is used to iterate over the output list
audio_files = []
for i, chunk in enumerate(audio_chunks):
    output_file = output_file_format.format(i)
    print(f"Exporting file {output_file}, duration {chunk.duration_seconds:6.2f}")
    chunk.export(output_file, format="wav")
    if chunk.duration_seconds > MAX_AUDIO_SECONDS_ALLOWED:
        print(f"{output_file} exceeded MAX_AUDIO_SECONDS_ALLOWED seconds {MAX_AUDIO_SECONDS_ALLOWED}, will not be processed further")
    else:
        audio_files.append({'file': output_file, 'duration': chunk.duration_seconds})


exit(0)

with open('out.txt', "w", encoding="utf-8") as f:
    for audio_file in audio_files:
        f.write(f"audio    : {audio_file['file']}")
        f.write('\n')

        f.write(f"duration : {audio_file['duration']:6.2f} secoonds")
        f.write('\n')

        json_response = get_text_from_audio(audio_file['file'])
        audio_file['text'] = json_response['text']
        audio_file['seconds'] = json_response['processingTime']

        f.write(audio_file['seconds'])
        f.write('\n')

        # f.write(audio_file['text'].encode('utf-8').decode(sys.stdout.encoding))
        f.write(audio_file['text'])
        f.write('\n\n')
