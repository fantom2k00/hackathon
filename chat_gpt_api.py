import openai

openai.api_key = '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'
model_engine = 'gpt-3.5-turbo'

def generateArticle(link):
    response = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Write article about " + link},
    ])
    message = response.choices[0]['message']
    return message['content']
