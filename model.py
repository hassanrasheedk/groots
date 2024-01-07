from flask import Flask, request, jsonify
import requests
import json
from gdelt import get_gdelt_news
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

# Ensure you have the necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

def extract_keywords(sentence):
    # Tokenize the sentence
    words = word_tokenize(sentence)

    # Remove stop words
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word.isalpha() and word not in stop_words]

    # Optional: Use POS tagging to select specific types of words
    tagged_words = pos_tag(filtered_words)
    keywords = [word for word, tag in tagged_words if tag.startswith(('NN'))]  # Nouns, Verbs, Adjectives, Adverbs

    return keywords

app = Flask(__name__)

def chat_with_gpt(prompt, model, country, business_phase):
    # Read the API key from config.json
    with open('config.json', 'r') as file:
        config = json.load(file)
    with open('evaluation_framework.json', 'r') as file:
        framework = json.load(file)
    
    framework_string = ""
    for key, value in framework.items():
        if key != "phase_analysis":
            for sub_key, sub_value in value.items():
                framework_string += sub_value + "\n"
        else:
            # Add only the selected phase's value
            framework_string += value[business_phase] + "\n"

    api_key = config['api_key']

    url = f"https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "messages": [{"role": "system", "content": f"You are a prompt analyser and consultant, you help the users generate better prompts using the provided frameworks, users will provide you with an idea and you will use the following framework to generate a set of relevant questions about the idea. {framework_string}"}, 
                     {"role": "user", "content": prompt}],
        "model": "gpt-3.5-turbo"
    }

    response = requests.post(url, headers=headers, json=data)
    response = response.json()

    questions = response['choices'][0]['message']['content']

    url = f"https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "messages": [{"role": "system", "content": f"You are an idea evaluator and consultant that evaluates ideas around circular economy and tells the user their pros and cons, and suggests improvements or changes if possible. Your suggestions should be anchored in some sources of truth and you should always provide reference documents or links that are from reputable institutions or companies."}, 
                     {"role": "user", "content": "Target Country: "+country+" "+prompt+"\n"+questions}],
        "model": model
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()

@app.route('/evaluate', methods=['POST'])
def evaluate():
    data = request.json

    prompt = data.get('prompt')
    model = data.get('model')
    country = data.get('country')
    business_phase = data.get('business_phase')

    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400
    elif not model:
        model = 'gpt-3.5-turbo'

    keywords = extract_keywords(prompt)
    top_articles, negative_score, positive_score = get_gdelt_news(keywords, country)

    print(top_articles)
    print(negative_score)
    print(positive_score)
    
    response = chat_with_gpt(prompt, model, country, business_phase)

    return jsonify(response['choices'][0]['message']['content'])

if __name__ == '__main__':
    app.run(debug=True)
