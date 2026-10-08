from ollama import chat
from memory.manager import MemoryManager
import json

memory = MemoryManager()

def extract_memory(user_input, facts):
    response = chat(
        model="qwen3.5:9b",
        messages=[
            {
                "role": "system",
                "content": f"""
            You are E.V.'s memory extraction system.

            Your ONLY job is to determine whether Ahmed's message contains
            a stable and useful personal fact that should be remembered.

            Existing stored facts:
            {json.dumps(facts, indent=2)}

            Save information such as:
            - personal preferences
            - favorite things
            - hobbies
            - skills
            - ongoing projects
            - long-term goals
            - useful permanent settings

            DO NOT save:
            - greetings
            - questions
            - temporary situations
            - random conversation
            - opinions about other people
            - information that is only relevant to the current conversation
            - instructions to E.V.
            - anything that is not clearly about Ahmed

            IMPORTANT:
            - If the new fact updates an existing fact, use the EXACT SAME KEY.
            - Do NOT create a new key for an existing concept.
            - Understand the meaning of the existing keys.
            - Only create a new key when the fact represents a genuinely new concept.

            Example:

            Existing fact:
            {{
                "favorite_color": "black"
            }}

            Ahmed says:
            "My favorite color is blue now."

            Return:
            {{
                "remember": true,
                "key": "favorite_color",
                "value": "blue"
            }}

            Another example:

            Existing fact:
            {{
                "favorite_superhero": "Spider-Man"
            }}

            Ahmed says:
            "I like Batman more now."

            Return:
            {{
                "remember": true,
                "key": "favorite_superhero",
                "value": "Batman"
            }}

            Return ONLY valid JSON.
            Do not use Markdown.
            Do not use ```.

            If there is a useful fact:

            {{
                "remember": true,
                "key": "short_snake_case_key",
                "value": "fact value"
            }}

            If there is no useful fact:

            {{
                "remember": false
            }}
            """
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    )

    content = response.message.content.strip()

    if not content:
        return {"remember": False}

    # Remove accidental Markdown code fences
    if content.startswith("```"):
        content = content.replace("```json", "")
        content = content.replace("```", "")
        content = content.strip()

    try:
        data = json.loads(content)

    except json.JSONDecodeError:
        return {"remember": False}

    # Validate the returned structure
    if not isinstance(data, dict):
        return {"remember": False}

    if data.get("remember") is True:
        if not data.get("key") or not data.get("value"):
            return {"remember": False}

        return {
            "remember": True,
            "key": str(data["key"]),
            "value": str(data["value"])
        }

    return {"remember": False}

def find_memory(user_input, facts):
    if not facts:
        return {"recall": False}

    response = chat(
        model="qwen3.5:9b",
        messages=[
            {
                "role": "system",
                "content": f"""
You are E.V.'s memory retrieval system.

Your ONLY job is to decide whether Ahmed's message
requires information from his stored personal facts.

Stored facts:
{json.dumps(facts, indent=2)}

Rules:

1. Recall a memory ONLY when Ahmed is asking about himself
   or information that can be answered using a stored fact.

2. Understand meaning, not exact wording.

For example, if the stored fact is:

"favorite_superhero": "Spider-Man"

These questions should recall it:
- What's my favorite superhero?
- Which superhero do I like?
- Who is my favorite hero?
- What superhero do I prefer?

3. Different wording can refer to the same memory.

For example, if the stored fact is:

"favorite_programming_language": "Python"

These may refer to the same fact:
- What's my favorite programming language?
- Which programming language do I like?
- What programming language do I prefer?

4. DO NOT recall memory for:
- general knowledge questions
- mathematical calculations
- questions about the world
- questions about other people
- unrelated questions
- information that cannot be answered from the stored facts

5. NEVER invent a key.

6. If a relevant memory exists:
Return ONLY:

{{
    "recall": true,
    "key": "exact_existing_key"
}}

7. If no relevant memory exists:
Return ONLY:

{{
    "recall": false
}}

IMPORTANT:
- The key MUST exactly match one of the stored keys.
- Return ONLY valid JSON.
- No Markdown.
- No explanations.
"""
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    )

    content = response.message.content.strip()

    if not content:
        return {"recall": False}

    if content.startswith("```"):
        content = content.replace("```json", "")
        content = content.replace("```", "")
        content = content.strip()

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        return {"recall": False}

    if not isinstance(data, dict):
        return {"recall": False}

    if data.get("recall") is True:
        key = data.get("key")

        if not isinstance(key, str):
            return {"recall": False}

        if key not in facts:
            return {"recall": False}

        return {
            "recall": True,
            "key": key
        }

    return {"recall": False}

def find_forget_memory(user_input, facts):
    keys = list(facts.keys())

    response = chat(
        model="qwen3.5:9b",
        messages=[
            {
                "role": "system",
                "content": f"""
You are E.V.'s memory deletion system.

Your job is to determine whether Ahmed wants to forget
one of his stored memories.

Stored memory keys:
{keys}

If Ahmed wants to forget a stored memory,
return ONLY:

{{
    "forget": true,
    "key": "exact_existing_key"
}}

If Ahmed does not want to forget anything,
return ONLY:

{{
    "forget": false
}}

IMPORTANT:
- The key MUST exactly match one of the stored keys.
- Understand the meaning of Ahmed's request.
- NEVER invent a key.
- Return ONLY valid JSON.
- No Markdown.
- No explanations.
"""
            },
            {
                "role": "user",
                "content": user_input
            }
        ]
    )
    content = response.message.content.strip()

    if not content:
        return {"forget": False}

    if content.startswith("```"):
        content = content.replace("```json", "")
        content = content.replace("```", "")
        content = content.strip()

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        return {"forget": False}

    if not isinstance(data, dict):
        return {"forget": False}

    if data.get("forget") is True:
        key = data.get("key")

        if not isinstance(key, str):
            return {"forget": False}

        if key not in facts:
            return {"forget": False}

        return {
            "forget": True,
            "key": key
        }

    return {"forget": False}