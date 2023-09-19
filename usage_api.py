from flask import Flask, request
import openai
import os


# set proxy to download model
proxy = 'http://proxy.kavosh.org:808'
os.environ['http_proxy'] = proxy
os.environ['HTTP_PROXY'] = proxy
os.environ['https_proxy'] = proxy
os.environ['HTTPS_PROXY'] = proxy

api_key = "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"
openai.api_key = api_key
system_prompt = "تو یک دستیار خیلی مفید هستی. وظیفه شما اصلاح  مغایرت املایی و تبدیل متن محاوره به رسمی در متن رونویسی شده فارسی است که معمولا شامل مبلغ به حروف و شماره کارت است. مطمئن شو که مبلغ حتما به عدد صحیح تبدیل شود واگر بین اعداد '-' وجود داشت آنها را حذف کن."


def generate_corrected_transcript(temperature, system_prompt, text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=temperature,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": text
            }
        ]
    )
    return response['choices'][0]['message']['content']


app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False


@app.route('/predict', methods=['POST'])
def prepare_text():

    outlist = {"text":""}
    # Loop over every file that the user submitted.
    for filename, handle in request.files.items():
        handle.save("./audio.ogg")

        audio_file = open("./audio.ogg", "rb")
        transcript = openai.Audio.transcribe("whisper-1", audio_file, prompt=system_prompt)
        handle.close()

        outlist["text"] = generate_corrected_transcript(0, system_prompt, transcript.text)


        # Return on a JSON format
    return outlist


@app.route('/check', methods=['GET'])
def check():
    return "every things right! "


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug= True)
