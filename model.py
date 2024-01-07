from flask import Flask, request, jsonify
# from openai import OpenAI
import requests
import json

app = Flask(__name__)

def chat_with_gpt(prompt, model):
    # Read the API key from config.json
    with open('config.json', 'r') as file:
        config = json.load(file)
    with open('evaluation_framework.json', 'r') as file:
        framework = json.load(file)
    
    framework_string = ""
    # Iterate through each section and value
    for section, content in framework.items():
        for key, value in content.items():
         framework_string = "\n".join([framework_string, value])

    print(framework_string)

    api_key = config['api_key']

    url = f"https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "messages": [{"role": "system", "content": f"You are a prompt analyser and consultant, you help the users generate better prompts using the provided frameworks, users will provide you with an idea and you will use the following framework to generate a set of relevant questions about the idea. {framework_string}"}, 
                     {"role": "user", "content": prompt}],
        "model": "gpt-3.5-turbo-16k"
    }

    response = requests.post(url, headers=headers, json=data)
    response = response.json()

    print(response['choices'][0]['message']['content'])
    questions = response['choices'][0]['message']['content']

    url = f"https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "messages": [{"role": "system", "content": f"You are an idea evaluator and consultant that evaluates ideas around circular economy and tells the user their pros and cons, and suggests improvements or changes if possible. Your suggestions should be anchored in some sources of truth and you should always provide reference documents or links that are from reputable institutions or companies."}, 
                     {"role": "user", "content": prompt+"\n"+questions}],
        "model": model
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

@app.route('/evaluate', methods=['POST'])
def evaluate():
    data = request.json
    prompt = data.get('prompt')
    model = data.get('model')
    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400
    elif not model:
        model = 'gpt-3.5-turbo'
    
    response = chat_with_gpt(prompt, model)
    print(response)
    return jsonify(response['choices'][0]['message']['content'])

if __name__ == '__main__':
    app.run(debug=True)
