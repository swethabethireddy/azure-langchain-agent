from agent_app import ask
import json

def init():
    pass

def run(data):
    try:
        input_data = json.loads(data)
        result = ask(input_data)
        return result
    except Exception as e:
        return {"error": str(e)}