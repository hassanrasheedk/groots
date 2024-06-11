from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
from gdelt import get_gdelt_news
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from typing import Dict, Tuple, List, Optional

app = Flask(__name__)
CORS(app)

# Ensure you have the necessary NLTK data
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('averaged_perceptron_tagger')

# Load configuration
with open('config.json', 'r') as file:
    config = json.load(file)
with open('evaluation_framework_1.json', 'r') as file:
    framework = json.load(file)

def extract_keywords(sentence: str) -> str:
    """
    Extracts keywords from a given sentence.

    Args:
        sentence (str): The input sentence from which to extract keywords.

    Returns:
        str: A string of extracted keywords separated by spaces.
    """
    words = word_tokenize(sentence)
    stop_words = set(stopwords.words('english'))
    filtered_words = [word for word in words if word.isalpha() and word not in stop_words]
    tagged_words = pos_tag(filtered_words)
    keywords = [word for word, tag in tagged_words if tag.startswith('NN')]  # Nouns
    return ' '.join(keywords[:5])

def generate_framework_string(business_phase: str) -> str:
    """
    Generates a framework string based on the given business phase.

    Args:
        business_phase (str): The business phase for which to generate the framework string.

    Returns:
        str: A formatted string based on the framework and business phase.
    """
    framework_string = ""
    for key, value in framework.items():
        if key != "phase_analysis":
            for sub_key, sub_value in value.items():
                framework_string += sub_value + "\n"
        else:
            framework_string += value[business_phase] + "\n"
    return framework_string

def chat_with_gpt(prompt: str, model: str, country: str, business_phase: str) -> Dict:
    """
    Interacts with the OpenAI GPT API using a given prompt.

    Args:
        prompt (str): The user prompt to send to GPT.
        model (str): The GPT model to use.
        country (str): The country context.
        business_phase (str): The business phase context.

    Returns:
        Dict: The response from the OpenAI API.
    """
    try:
        framework_string = generate_framework_string(business_phase)
        api_key = config['api_key']
        url = "https://api.openai.com/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "messages": [{"role": "system", "content": f"{framework_string}"}, 
                         {"role": "user", "content": prompt}],
            "model": model
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code != 200:
            raise Exception("Failed to get response from OpenAI API")
        return response.json()
    except Exception as e:
        return {"error": str(e)}

@app.route('/evaluate', methods=['POST'])
def evaluate() -> Tuple:
    """
    Flask route to evaluate a prompt using GPT and GDELT news data.

    Returns:
        Tuple: The response JSON and HTTP status code.
    """
    data = request.json
    prompt = data.get('prompt')
    model = data.get('model', 'gpt-3.5-turbo')
    country = data.get('country')
    business_phase = data.get('business_phase')

    if not prompt:
        return jsonify({'error': 'No prompt provided'}), 400

    keywords = extract_keywords(prompt)
    top_articles, negative_score, positive_score = get_gdelt_news(keywords, country)
    
    gpt_response = chat_with_gpt(prompt, model, country, business_phase)
    if 'error' in gpt_response:
        return jsonify({'error': gpt_response['error']}), 500

    response = {
        "llm_response": gpt_response['choices'][0]['message']['content'],
        "top_articles": top_articles,
        "negative_score": negative_score,
        "positive_score": positive_score
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)