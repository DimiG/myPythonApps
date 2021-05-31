#!/usr/bin/env python
# -*- coding: utf-8 -*-
# =============================================================================
# Author      : Dmitri G.
# Version     : 1.0.0
# Date        : 2021/05/31
# FileName    : recognize.py
# Description : Audio transcription program
# =============================================================================

# Import Libraries
import os                                   # Standard library
import sys                                  # Standard library
import argparse
import speech_recognition as sr
from pydub import AudioSegment
from pydub.silence import split_on_silence


# Create a speech recognition object
r = sr.Recognizer()


def get_audio_transcription(f):
    """
    Splitting the large audio file into chunks
    and apply speech recognition on each of these chunks
    """

    # Variables Setup
    folder_name = "audio-chunks"            # Folder name for chunks

    # Open the audio file using pydub
    sound = AudioSegment.from_wav(f)

    # Split audio sound where silence is 700 miliseconds or more and get chunks
    chunks = split_on_silence(sound,
                              # Experiment with this value for your target audio file
                              min_silence_len=500,
                              # Adjust this per requirement
                              silence_thresh=sound.dBFS - 14,
                              # Keep the silence for 1 second, adjustable as well
                              keep_silence=500,
                              )

    # Create a directory to store the audio chunks
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    whole_text = ""

    # Process each chunk
    for i, audio_chunk in enumerate(chunks, start=1):

        # Export audio chunk and save it in
        # The `folder_name` directory
        chunk_filename = os.path.join(folder_name, f"chunk{i}.wav")
        audio_chunk.export(chunk_filename, format="wav")

        # Recognize the chunk
        with sr.AudioFile(chunk_filename) as source:
            #  To denoise the sound use the command below
            #  r.adjust_for_ambient_noise(source, duration=0.3)
            audio_listened = r.record(source)

            # Try converting it to text and print it
            try:
                text = r.recognize_google(audio_listened, language="en-US")
            except sr.UnknownValueError as e:
                print("Error:", str(e))
            else:
                text = f"{text.capitalize()}. "
                print(chunk_filename, ":", text)
                whole_text += text

    # Print the text for all chunks detected
    print(whole_text)


def main():
    #  Get the argument with audio file name
    parser = argparse.ArgumentParser(
        prog='recognize',
        description=(
            '*** Speech recognize program v1.0, Author: Dmitri G. 2021 ***'),
        epilog='*** You MUST enable Internet connection before run this program! ***')
    parser.add_argument('filename', nargs=1,
                        help='WAV filename you wanna work with')
    args = parser.parse_args()
    fname = args.filename[0]
    # A function that splits the audio file into chunks
    # and applies speech recognition
    get_audio_transcription(fname)


if __name__ == "__main__":
    main()
