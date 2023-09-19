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
audio_file= open("audio_2023-09-12_17-16-36.ogg", "rb")
transcript = openai.Audio.transcribe("whisper-1", audio_file)

system_prompt = "You are a helpful assistant . Your task is to correct any spelling discrepancies in the transcribed text Persian.Make sure that the names of the following products are spelled correctly: "
# system_prompt = " حرف سین رو به صاد تبدیل کن. هر کلمه ای که معنی عدد میدهد را به عدد صحیح تبدیل کن و اگر تومن یا تو من داخل متن بود و همچنین اعداد رو بدون هیچ علامتی پشت سر هم بنویس."
# system_prompt = "do this post processing in the persian for input text, first find the word that present number in persian and then convert it to integer. secound delete every character between numbers"
system_prompt = "تو یک دستیار خیلی مفید هستی. وظیفه شما اصلاح  مغایرت املایی و تبدیل متن محاوره به رسمی در متن رونویسی شده فارسی است که معمولا شامل مبلغ به حروف و شماره کارت است. مطمئن شو که مبلغ حتما به عدد صحیح تبدیل شود و شماره کارت بدون هیچ کاراکتر اضافی نمایش داده شود."
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

corrected_text = generate_corrected_transcript(0, system_prompt, transcript.text)
print(transcript.text)
print(corrected_text)