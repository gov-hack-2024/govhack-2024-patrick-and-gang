from pathlib import Path
from openai import OpenAI
from gtts import gTTS
import os

def text_to_speech(input_text,output_path = 'output.mp3',play = True):

    # Convert text to speech
    tts = gTTS(input_text)

    # Save the speech as an MP3 file
    tts.save(output_path)

    if play:
        # Play the audio (optional)
        os.system("start output.mp3")


if __name__ == '__main__':


    # Text to be converted into speech
    text = "New VLocity Trains Since July 2022, we have delivered 10 new VLocity trains. These trains include the last standard-gauge trains for the North East Line and the 100th VLocity train, which rolled out in September 2022.A standard-gauge train fits on tracks that are 1,435 millimetres wide. Delivery of the 12 VLocity trains funded in the 2022–23 State Budget is currently underway, continuing the rollout of these faster, smoother and more reliable trains"

    text_to_speech(text)



    # client = OpenAI()
    # speech_file_path = Path(__file__).parent / "speech.mp3"
    # response = client.audio.speech.create(
    #   model="tts-1",
    #   voice="alloy",
    #   input="Today is a wonderful day to build something people love!"
    # )
    #
    # response.stream_to_file(speech_file_path)