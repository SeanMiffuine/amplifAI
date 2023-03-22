import sys
import azure.cognitiveservices.speech as speechsdk
from keys import *

    
# python 3.7 is needed for azure cognitive speech services
def text_to_speech(text):
    speech_config = speechsdk.SpeechConfig(subscription= subscription, region='westus')
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

    # The language of the voice that speaks.
    speech_config.speech_synthesis_voice_name='en-US-JennyNeural'

    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    
    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized for text [{}]".format(text))
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
                print("Did you set the speech resource key and region values?")

def speech_recognize_continuous_async_from_microphone():
    """performs continuous speech recognition asynchronously with input from microphone"""
    speech_config = speechsdk.SpeechConfig(subscription=subscription, region="westus")
    speech_config.endpoint_id = endpoint # endpoint to use speech model
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

    done = False

    def recognized_cb(evt: speechsdk.SpeechRecognitionEventArgs):

        print(evt.result.text)
        text_to_speech(evt.result.text)
        if evt.result.text == "Stop.":
            speech_recognizer.stop_continuous_recognition_async()

        #print('RECOGNIZED: {}'.format(evt))

    def stop_cb(evt: speechsdk.SessionEventArgs):
        """callback that signals to stop continuous recognition"""
        print('CLOSING on {}'.format(evt))
        nonlocal done
        done = True

    # Connect callbacks to the events fired by the speech recognizer
    #speech_recognizer.recognizing.connect(recognizing_cb)
    speech_recognizer.recognized.connect(recognized_cb)
    speech_recognizer.session_stopped.connect(stop_cb)
    speech_recognizer.canceled.connect(stop_cb)

    # Perform recognition. `start_continuous_recognition_async asynchronously initiates continuous recognition operation,
    # Other tasks can be performed on this thread while recognition starts...
    # wait on result_future.get() to know when initialization is done.
    # Call stop_continuous_recognition_async() to stop recognition.
    result_future = speech_recognizer.start_continuous_recognition_async()

    result_future.get()  # wait for voidfuture, so we know engine initialization is done.
    print('Continuous Recognition is now running, say something.')

    while not done:
        # No real sample parallel work to do on this thread, so just wait for user to type stop.
        # Can't exit function or speech_recognizer will go out of scope and be destroyed while running.
        print('type "stop" then enter when done')
        stop = input()
        if (stop.lower() == "stop"):
            print('Stopping async recognition.')
            speech_recognizer.stop_continuous_recognition_async()
            #break

    print("recognition stopped, main thread can exit now.")


speech_recognize_continuous_async_from_microphone()

