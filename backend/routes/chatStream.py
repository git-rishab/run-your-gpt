import asyncio
import json
import sys
from flask import request, jsonify, send_file
from gtts import gTTS
import os
import openai
import speech_recognition as sr
from pydub import AudioSegment
from config.db import user

try:
    import websockets
except ImportError:
    print("Websockets package not found. Make sure it's installed.")

# For local streaming, the websockets are hosted without ssl - ws://
HOST = 'subscription-tribute-interaction-capture.trycloudflare.com'
URI = f'ws://{HOST}/api/v1/chat-stream'

# For reverse-proxied streaming, the remote will likely host with ssl - wss://
# URI = 'wss://your-uri-here.trycloudflare.com/api/v1/stream'

history = {'internal': [], 'visible': []}

async def run(user_input, history):
    # Note: the selected defaults change from time to time.
    request = {
        'user_input': user_input,
        'max_new_tokens': 250,
        'auto_max_new_tokens': False,
        'history': history,
        'mode': 'instruct',  # Valid options: 'chat', 'chat-instruct', 'instruct'
        'character': 'Example',
        'instruction_template': 'Vicuna-v1.1',  # Will get autodetected if unset
        'your_name': 'You',
        # 'name1': 'name of user', # Optional
        # 'name2': 'name of character', # Optional
        # 'context': 'character context', # Optional
        # 'greeting': 'greeting', # Optional
        # 'name1_instruct': 'You', # Optional
        # 'name2_instruct': 'Assistant', # Optional
        # 'context_instruct': 'context_instruct', # Optional
        # 'turn_template': 'turn_template', # Optional
        'regenerate': False,
        '_continue': False,
        'chat_instruct_command': 'Continue the chat dialogue below. Write a single reply for the character "<|character|>".\n\n<|prompt|>',

        # Generation params. If 'preset' is set to different than 'None', the values
        # in presets/preset-name.yaml are used instead of the individual numbers.
        'preset': 'None',
        'do_sample': True,
        'temperature': 0.7,
        'top_p': 0.1,
        'typical_p': 1,
        'epsilon_cutoff': 0,  # In units of 1e-4
        'eta_cutoff': 0,  # In units of 1e-4
        'tfs': 1,
        'top_a': 0,
        'repetition_penalty': 1.18,
        'repetition_penalty_range': 0,
        'top_k': 40,
        'min_length': 0,
        'no_repeat_ngram_size': 0,
        'num_beams': 1,
        'penalty_alpha': 0,
        'length_penalty': 1,
        'early_stopping': False,
        'mirostat_mode': 0,
        'mirostat_tau': 5,
        'mirostat_eta': 0.1,
        'guidance_scale': 1,
        'negative_prompt': '',

        'seed': -1,
        'add_bos_token': True,
        'truncation_length': 2048,
        'ban_eos_token': False,
        'skip_special_tokens': True,
        'stopping_strings': []
    }

    async with websockets.connect(URI, ping_interval=None) as websocket:
        await websocket.send(json.dumps(request))

        while True:
            incoming_data = await websocket.recv()
            incoming_data = json.loads(incoming_data)

            match incoming_data['event']:
                case 'text_stream':
                    yield incoming_data['history']
                case 'stream_end':
                    return


async def print_response_stream(user_input, history):
    cur_len = 0
    generated_messages = []
    async for new_history in run(user_input, history):
        cur_message = new_history['visible'][-1][1][cur_len:]
        cur_len += len(cur_message)
        generated_messages.append(cur_message)
        # sys.stdout.flush()  # If we don't flush, we won't see tokens in realtime.
    collected_responses = ''.join(generated_messages)  # Combine all messages
    return collected_responses


def chat():
    prompt = request.json['prompt']
    user_id = request.json['id']
    limit = request.json['limit']
    collected_responses = asyncio.run(print_response_stream(prompt, history))
    # history['internal'].append(prompt)
    # history['visible'].append(collected_responses)
    updated = user.update_one({'_id':user_id}, {'$set':{'limit':limit-1}})
    return jsonify({"ok":True, "message":collected_responses})

def audio():
    try:
        request_data = request.get_json()
        text = request_data.get('prompt')  # Access the 'prompt' value from the dictionary
        
        # Convert text to speech using gTTS
        tts = gTTS(text=text, lang='en')
        
        # Save the generated speech as an audio file
        audio_file_path = 'speech.mp3'
        tts.save(audio_file_path)
        
        # Send the audio file back to the client
        return send_file(audio_file_path, as_attachment=True)
    except Exception as e:
        return str(e), 500

def audio_to_text():
    try:
        audio_file = request.files['audio']

        # Convert audio to WAV format
        converted_audio = "converted_audio.wav"
        audio = AudioSegment.from_file(audio_file)

        # Print the length of the audio for debugging
        print("Audio Length:", len(audio), "milliseconds")

        audio.export(converted_audio, format="wav")

        # Check if the converted audio file exists
        if os.path.exists(converted_audio):
            print("Converted Audio File Created:", converted_audio)
        else:
            print("Converted Audio File Not Created")

        recognizer = sr.Recognizer()
        with sr.AudioFile(converted_audio) as source:
            audio_data = recognizer.record(source)  # Record audio from the file

        # Recognize the audio
        text = recognizer.recognize_google(audio_data)

        # Clean up by deleting the converted audio file
        os.remove(converted_audio)

        return jsonify({'text': text})
    except Exception as e:
        return str(e), 500


