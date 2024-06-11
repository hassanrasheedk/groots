# Groots - Sustainable LLM

Groots is an AI assistant designed to evaluate ideas and provide comprehensive evaluations based on a set of predefined criteria. Users can also input their own criteria for specific evaluations. The system refines the initial user prompt, creating better-engineered prompts using state-of-the-art techniques.

Created by Zoey Yan, Konstantina Yaneva, and Hassan Rasheed

## Product Mockup
Check out the product mockup on [Figma](https://www.figma.com/proto/Tmn1XLPHLMgVBnOtfNIaNJ/AI-EarthHack?page-id=0%3A1&type=design&node-id=1-2&viewport=492%2C169%2C0.15&t=749bjuNExNLZGM1a-1&scaling=scale-down&starting-point-node-id=1%3A2&mode=design)

## Project Overview
Groots is built to help users evaluate innovative ideas, particularly in the context of sustainability and circular economy concepts. The AI assistant leverages advanced language models to generate insightful and detailed evaluations based on both preset and user-defined criteria.

### Key Features
- **Predefined Criteria Framework**: Uses a preset framework for idea evaluation.
- **Custom Criteria Input**: Allows users to input their own specific criteria for evaluation.
- **Prompt Refinement**: Enhances initial user prompts to generate more precise and effective evaluations.
- **Integration with GDELT API**: Fetches relevant news articles and sentiment analysis from the GDELT database.

## Setup Requirements
To run this project, you will need the following software installed:

- Node.js
- Python
- Angular CLI

## Frontend Setup
1. Navigate to the `groots-frontend` directory:
    ```sh
    cd groots-frontend
    ```

2. Install the required Node.js packages:
    ```sh
    npm install
    ```

## Backend Setup
1. Navigate to the project directory:
    ```sh
    cd groots
    ```

2. Install the required Python packages:
    ```sh
    pip install -r requirements.txt
    ```

3. Configure the API key:
    - Open `config.json` in the project directory.
    - Add your OpenAI API key:
        ```json
        {
            "api_key": "your_openai_api_key"
        }
        ```

    Alternatively, you can configure the system to use an open-source model if preferred.

## Starting the Frontend
1. Ensure you are in the `groots-frontend/groots-spa` directory.
2. Start the Angular development server:
    ```sh
    ng serve
    ```

## Starting the Backend
1. Ensure you are in the project directory.
2. Start the Flask server:
    ```sh
    python model.py
    ```

## Usage
Once both the frontend and backend servers are running, you can access the application via your web browser at `http://localhost:4200`. 

## Contributing
Contributions are welcome! Please fork the repository and create a pull request with your changes.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
