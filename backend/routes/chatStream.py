import asyncio
import json
import sys
from flask import request, jsonify, send_file
from gtts import gTTS
import os
import openai
from config.db import user
import tempfile
from pydub import AudioSegment
from bson import ObjectId

try:
    import websockets
except ImportError:
    print("Websockets package not found. Make sure it's installed.")

# For local streaming, the websockets are hosted without ssl - ws://
HOST = 'shown-provinces-barriers-creating.trycloudflare.com'
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
    user_id = ObjectId(request.json['id'])
    limit = request.json['limit']
    collected_responses = asyncio.run(print_response_stream(prompt, history))
    # history['internal'].append(prompt)
    # history['visible'].append(collected_responses)
    print(user_id, limit)
    updated = user.update_one({'_id':user_id}, {'$set':{'limit':limit-1}})
    if updated.acknowledged:
        print("Update acknowledged")
    else:
        print("Update not acknowledged")
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
        
        if audio_file and allowed_file(audio_file.filename, {'wav', 'webm'}):
            temp_dir = tempfile.gettempdir()
            temp_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploaded_audio.wav')
            audio_file.save(temp_path)
            openai.api_key = os.getenv('OPEN_AI_KEY')
            audio_file= open(f"{os.path.dirname(os.path.abspath(__file__))}\\uploaded_audio.wav", "rb")
            transcript = openai.Audio.transcribe("whisper-1", audio_file)
            print(transcript)
            return jsonify({'ok':True})
        else:
            return jsonify({"error": "Invalid file format"}), 400
    except Exception as e:
        print("Error:", str(e))
        return jsonify({"error": str(e)}), 500

def allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions




