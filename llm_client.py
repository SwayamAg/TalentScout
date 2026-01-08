from openai import AzureOpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION")
)


def get_llm_response(messages, temperature=0.3):
    response = client.chat.completions.create(
        model=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"),  
        messages=messages,
        temperature=temperature
    )
    return response.choices[0].message.content

# print(os.getenv("AZURE_OPENAI_ENDPOINT"))
# print(os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME"))
# print(os.getenv("AZURE_OPENAI_API_VERSION"))
