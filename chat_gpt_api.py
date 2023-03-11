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
