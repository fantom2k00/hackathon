import openai

def generateArticle(link):
    openai.api_key = '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'
    model_engine = 'gpt-3.5-turbo'
    response = openai.ChatCompletion.create(
    model='gpt-3.5-turbo',
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Write article about " + link},
    ])
    message = response.choices[0]['message']
    return message['content']
