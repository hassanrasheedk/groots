import openai
import os

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

client = openai.OpenAI(api_key='')


def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0
    )
    return response.choices[0].message.content



import os
from langchain.document_loaders import PyPDFLoader
from langchain.agents import load_tools
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from langchain.llms import OpenAI

os.environ["OPENAI_API_KEY"] = ''

llm = OpenAI(temperature=0)
tools = load_tools(["serpapi", "llm-math"], llm=llm, serpapi_api_key="753c4a973372093745cd0f89af65e1ddba549c2d925921083c3d8f1a1f97322b")
agent = initialize_agent(tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True)

idea = f""" Woven fabrics: Hair can be woven into fabrics to create clothing items such as shawls, scarves, and blankets. Knitted garments: Hair can be knitted into garments such as sweaters, hats, and scarves.
"""
prompt = f"""

summarize idea in a concise sentence of the product or service idea: ```{idea}``` 
"""
summary = get_completion(prompt)
print(summary)


def evaluate_idea(agent, idea, summary, question, output_description):
    # Generate the question
    full_question = f"{question} {summary}."
    answer = agent.run(full_question)

    # Generate the prompt
    prompt = f"""
    You are an idea evaluator and consultant that evaluates ideas around circular economy and tells the user their pros and cons, and suggests improvements or changes if possible. Your suggestions should be anchored in some sources of truth, and you should always provide reference documents or links that are from reputable institutions or companies.
    If you don't know the answer, just say that you don't know; don't try to make up an answer. Don't be overly optimistic, but try to evaluate the idea objectively.

    Consider answer. {output_description}
    Answer = ```{answer}```
    Idea: ```{idea}``` 
    Output in bullet points.
    """
    
    # Get the completion and print the response
    response = get_completion(prompt)
    print(response)


# Example usage
evaluate_idea(agent, idea, summary, "Investigate the development process of similar products or services like", "How does the idea align with trends in identified in the answer.")

evaluate_idea(agent, idea, summary, "Identify other products or services that are similar to the", "What are the similarities and differences between the idea and the existing products in the answer.")

evaluate_idea(agent, idea, summary, "What are specific current trends in the development of ideas like", "Consider the two answers. Consider the trends identified in the answers. Consider other historical tensions, legislation, or politics. How can these factors may impact the understanding of needs. How can these factors may impact the shaping of goals for the new business idea.")

evaluate_idea(agent, idea, summary, "What are specific past trends in the development of ideas like", "Consider the two answers. Consider the trends identified in the answers. Consider other historical tensions, legislation, or politics. How can these factors may impact the understanding of needs. How can these factors may impact the shaping of goals for the new business idea.")

evaluate_idea(agent, idea, summary, "Other businesses or initiatives in the same domain as", "Think about past failures in similar businesses or initiatives in that domain. Identify barriers that can be expected based on past failures that make it difficult to include circular goals in the business idea.")

evaluate_idea(agent, idea, summary, "What are the existing market and industry practices in the same domain as", "Consider the potential impact of the idea on the existing market and industry practices. How will the idea disrupt or improve current practices? Output in bullet points.")

evaluate_idea(agent, idea, summary, "Find out the most recent updates on the rules for the same domain as", "")
