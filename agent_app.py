from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv

from langchain.agents import initialize_agent, load_tools
from langchain.chat_models import AzureChatOpenAI

load_dotenv()

llm = AzureChatOpenAI(
    deployment_name=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
    model_name=os.getenv("AZURE_OPENAI_MODEL", "gpt-35-turbo"),
    openai_api_key=os.getenv("AZURE_OPENAI_API_KEY"),
    openai_api_version="2023-07-01-preview",
    openai_api_base=os.getenv("AZURE_OPENAI_ENDPOINT"),
)

tools = load_tools(["serpapi"])
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

app = FastAPI()

class AgentInput(BaseModel):
    question: str

@app.post("/ask")
def ask(input: AgentInput):
    try:
        response = agent.run(input.question)
        return {"response": response}
    except Exception as e:
        return {"error": str(e)}