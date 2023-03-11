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
