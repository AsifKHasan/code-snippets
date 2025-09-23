#!/usr/bin/env python
"""
    given path to audio file and 
    and optional reference text, 
    this script returns recognized text 
    transcription, ASR engine processing 
    and similarity to reference text

Example:

$ ./asr_test_commandline.py --audio-file-path /home/dipto/Downloads/celloscope/asr/audio-recorder-web-v2/audio-recorder-web/test.wav --reference-text="এখন আগের চেয়ে অনেক কম সময় লাগছে"

output:

recognized text : "এখন আগের চেয়ে অনেক কম সময় লাগছে"
Processing took 1.74 seconds
Similarity with reference text is 100.0%

"""
import os
import json
import argparse
import requests

my_parser = argparse.ArgumentParser()
my_parser.add_argument('--audio-file-path', type=str, required=True)
my_parser.add_argument('--reference-text', type=str, required=False)
args = my_parser.parse_args()


def get_text_transcript(audio_file_path, reference_text=None):
    request_json = {
        'files': open(audio_file_path, 'rb')
    }

    response = requests.post(
        "https://nlp.celloscope.net/nlp/dataset/v1/audio/speech-to-text",
        data={'referenceText' : reference_text},
        files=request_json
    )

    json_response = json.loads(response.text)
    transcript = json_response['text']
    processing_time = json_response['processingTime']
    similarity = json_response['similarity']

    print(f'recognized text : "{transcript}"')
    print(processing_time)
    if similarity != '0%' :
        print(f"Similarity with reference text is {similarity}")



if __name__ == "__main__":
    get_text_transcript(audio_file_path=args.audio_file_path, reference_text=args.reference_text)



