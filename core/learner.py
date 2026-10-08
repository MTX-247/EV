from ollama import chat
import json


def learn(information):
    prompt = f"""
    Information: {information}
    Decide if this information is useful, stable, and worth remembering as knowledge.
    If it is useful, determine the most appropriate topic yourself.

    Return JSON only in this format:

    {{
        "learn": true,
        "topic": "...",
        "knowledge": "..."
    }}

    If the information is not worth remembering, return:

    {{
        "learn": false
    }}

    Do not include any explanation outside the JSON.
    """
    response = chat(
        model="qwen3.5:9b",
        messages=[
            {"role": "user", "content": prompt}
        ],
    )

    print(response.message.content)
    result = response.message.content
    result =json.loads(result)
    return result