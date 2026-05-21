import json
from tools.search import search_web
from tools.calculator import calculate
from tools.weather import get_weather
from config import MAX_ITERATIONS, MODEL
from openai import OpenAI, OpenAIError
from dotenv import load_dotenv
import os
import httpx
os.environ["NO_PROXY"] = "*"

TOOL_MAP = {
    "search_web": search_web,
    "calculate": calculate,
    "get_weather": get_weather,
}

tools = [
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Search the internet for current information, recent news, facts, or any topic that requires up-to-date data. Use this when the user asks about recent events or information you don't know.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query to look up. Be specific and concise, like a Google search query."
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Number of results to return. Default is 3. Use more for broader research."
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Fetch the current weather conditions for a given city. Use this when the user asks about the weather, temperature, or climate in a specific location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The city name in English, e.g. 'Paris', 'London', 'New York'."
                    }
                },
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluate a mathematical expression and return the result. Use this for arithmetic, percentages, or any numerical calculation. Input must be a valid Python math expression like '2 + 2' or '(15 * 8) / 3'.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "A valid Python mathematical expression, e.g. '2 + 2', '(15 * 8) / 3', 'round(3.14159, 2)'."
                    }
                },
                "required": ["expression"]
            }
        }
    }
]

load_dotenv()

client = OpenAI(
    base_url="http://127.0.0.1:11434/v1",
    api_key="ollama",
    http_client=httpx.Client(proxy=None),
)

def run_agent(user_message: str, history: list[dict]) -> str:
    history.append({"role":"user", "content":user_message})
    for _ in range(MAX_ITERATIONS):
        response = client.chat.completions.create(
            model=MODEL,
            messages=history,
            tools=tools,
            tool_choice="auto"
        )
        
        message = response.choices[0].message
        
        if message.tool_calls:
            tool_call = message.tool_calls[0]
            tool_name = tool_call.function.name
            tool_args = json.loads(tool_call.function.arguments)
            history.append(message)
            info = TOOL_MAP[tool_name](**tool_args)
            history.append({"role": "tool", "tool_call_id": tool_call.id, "content": info}),
        else:
            return message.content
    
    return "I could not find an answer after several attempts."