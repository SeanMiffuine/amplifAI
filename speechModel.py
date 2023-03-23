import azure.cognitiveservices.speech as speechsdk
import os
from keys import *

# values
RESET = "\033[0m"
BOLD = "\033[1m"
UNDERLINE = "\033[4m"
REVERSE = "\033[7m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"


# python 3.7 is needed for azure cognitive speech services
def text_to_speech(text):
    speech_config = speechsdk.SpeechConfig(subscription= subscription, region='westus')
    audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

    # The language of the voice that speaks.
    speech_config.speech_synthesis_voice_name='en-US-JennyNeural'
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        None
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        #print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        None
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
        print("\n")
        print(f"\t{BOLD}{CYAN}{evt.result.text}{RESET}")
        #print(evt.result.text)
        text_to_speech(evt.result.text)
        
        if evt.result.text == "Stop speech model.":
            speech_recognizer.stop_continuous_recognition_async()
            return

        #print('RECOGNIZED: {}'.format(evt))

    def stop_cb(evt: speechsdk.SessionEventArgs):
        """callback that signals to stop continuous recognition"""
        #print('CLOSING on {}'.format(evt))
        print("\tClosed Speech Model")
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
    #print('Continuous Recognition is now running, say something.')

    while not done:
        # No real sample parallel work to do on this thread, so just wait for user to type stop.
        # Can't exit function or speech_recognizer will go out of scope and be destroyed while running.
        #print('type "stop" then enter when done')
        stop = input()
        speech_recognizer.stop_continuous_recognition_async()
        #break

    #print("recognition stopped, main thread can exit now.")

def clear_screen():
    os.system("cls")

def print_header():
    print(f"{BOLD}{BLUE}{'=' * 80}{RESET}")
    print(f"{BOLD}{BLUE}{'*' * 80}{RESET}")
    print(f"{BOLD}{BLUE}{'=' * 80}{RESET}")


def print_intro():
    print("\n" * 3)
    print(f"{BOLD}{CYAN}{' ' * 36 + 'AmplifAI'}{RESET}")
    print(f"{BOLD}{CYAN}{' ' * 28 + 'By Yeojun, Iris, and Sean'}{RESET}")

def print_menu():
    print("\n")
    print(f"\t\t\t\t{RESET}{CYAN}[ BEGIN or EXIT ]{RESET}")

def transcription():
    print("\n\n\tTranscription:\n")

def print_footer():
    print("\n" * 3)
    print(f"{BOLD}{BLUE}{'=' * 80}{RESET}")
    print(f"{BOLD}{BLUE}{'*' * 80}{RESET}")
    print(f"{BOLD}{BLUE}{'=' * 80}{RESET}")


def init():
    while True:
        clear_screen()
        print_header()
        print_intro()
        print_menu()
        print_footer()
        choice = input()
        if choice == "EXIT":
            quit()
        elif choice == 'BEGIN':
            clear_screen()
            print_header()
            transcription()
            speech_recognize_continuous_async_from_microphone()

    
init()

