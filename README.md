# groots
An AI assistant that evaluates ideas and provides evaluations based on provided criteria, we have a preset of criteria framework and also allow user to input their own criteria if they wish to, we also take the initial user prompt and create better engineered prompts based on SOTA techniques.

Created by Zoey Yan, Konstantina Yaneva, and Hassan Rasheed

Product Mockup: https://www.figma.com/proto/Tmn1XLPHLMgVBnOtfNIaNJ/AI-EarthHack?page-id=0%3A1&type=design&node-id=1-2&viewport=492%2C169%2C0.15&t=749bjuNExNLZGM1a-1&scaling=scale-down&starting-point-node-id=1%3A2&mode=design


## Setup Requirements
```
Node.js
Python
Angular
```

## Backend Installation
1. Go to groots-frontend directory
```
npm install
```
3. Go to project directory
```
pip install -r requirements.txt
```

## Starting Frontend:
```
ng-serve
```

##Start Backend
```
python model.py
```

You have to enter your OpenAI api_key into config.json. Or switch to an open source model if you like.
