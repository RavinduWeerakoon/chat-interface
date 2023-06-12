import flask
import openai
import base64
from flask import Flask, render_template, request
import requests
import os
openai.api_key = os.environ.get("API_KEY").strip()

app = Flask(__name__)

AUTHORIZATION = "26dec25a04f44924a5bddcd05a4d91e7"
X_USER_ID = "Z6zSIj8yDWQzLl25dud3b03TW2K2"

url_1 = "https://play.ht/api/v1/convert"
url_2 = "https://play.ht/api/v1/articleStatus?transcriptionId="
payload = {
    "content": ["Hello world"],
    "voice": "en-US-JennyNeural"
}
header_1 = {
    "accept": "application/json",
    "content-type": "application/json",
    "AUTHORIZATION": AUTHORIZATION,
    "X-USER-ID": X_USER_ID
}

header_2 = {
    "accept": "application/json",
    "AUTHORIZATION": AUTHORIZATION,
    "X-USER-ID": X_USER_ID
}

def convert(text):
    payload["content"] = [text]
    response = requests.post(url_1, json=payload, headers=header_1)
    t_id = response.json()["transcriptionId"]
    
    voice_url = url_2 + t_id
    url_response = requests.get(voice_url, headers=header_2)
    
    return url_response.json()["audioUrl"]

def think(text):
    """
    Generates a response to the user's input.
    """
    
    # Send the conversation to the GPT API

    response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"give me some information on point form abotu {text}. Don't make it too long. and keep the information in point form spearte each points by br tags",
            max_tokens=500,
            top_p=1,
            frequency_penalty=0.8,
            presence_penalty=1,
            # stop=["<h"]
        )

    # Extract the assistant's response from the API response
    message = response.get("choices")[0]['text']
    
    
    return message

@app.route('/')
def main():
    return render_template('index.html')


@app.route('/whisper', methods=['POST'])
def completion_api():
    
    data = request.files['audio_data'].read()
    with open('audio.webm', 'wb') as f:
        f.write(data)
    audio_file = open('audio.webm', "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)
    details = think(transcript)
    

    url = convert(details[:100])
    url = url.split("?")[0]
    print(url)
    return url
    
@app.route('/completions', methods=['POST'])
def completion():
    json = request.json
    completion = openai.Completion.create(engine="text-davinci-003", prompt=request.prompt)
    return flask.Response(completion)


if __name__ == '__main__':
    app.run(debug=True,port=3389)

# print(convert("hello world"))

