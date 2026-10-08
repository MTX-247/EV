from ollama import chat
import json


def plan(user_input, facts, knowledge_topics):
    prompt = f"""
    You are E.V.'s Planner.

    Your job is to analyze the user's message and determine which available
    resources E.V. needs in order to answer the message correctly.

    You do NOT answer the user.
    You do NOT execute tools.
    You only create a structured plan describing what E.V. needs.

    User message:
    {user_input}

    Available personal memory:
    {list(facts.keys())}

    Available knowledge:
    {knowledge_topics}


    AVAILABLE RESOURCES

    1. Memory
    Memory contains stable personal information about Ahmed.

    Use Memory when the user's request requires information specifically about
    Ahmed that may already be stored.

    Examples:
    - "What is my favorite programming language?" → Memory
    - "Do you remember what I like?" → Memory
    - "What project am I working on?" → Memory

    Do NOT use Memory for general facts about the world.


    2. Knowledge
    Knowledge contains information E.V. already knows about the world.

    Use Knowledge when the answer can be provided from one of the available
    knowledge topics.

    Examples:
    - "What is Python?" → Knowledge: Python
    - "Explain recursion." → Knowledge: Recursion
    - "What is photosynthesis?" → Knowledge: Photosynthesis

    Only request a Knowledge topic that actually exists in Available knowledge.


    3. Tools
    Tools allow E.V. to perform actions or calculations.

    Use a Tool when the user's request requires an operation that should be
    performed instead of simply answering from reasoning or stored information.

    Examples:
    - "Calculate 25 * 4." → Tool: calculate
    - "What is 1234 * 5678?" → Tool: calculate

    Only request tools that are actually available.


    4. No resource
    Sometimes the user's message does not require Memory, Knowledge, or Tools.

    In that case, no resource is needed and the Brain can answer directly.

    Examples:
    - "Explain recursion in a simple way." → No resource
    - "What do you think about this idea?" → No resource


    MULTIPLE RESOURCES

    The user may need more than one resource in the same request.

    Do NOT assume that only one resource can be selected.

    Examples:

    "Do I like Python, and what is Python?"
    → Memory + Knowledge: Python

    "What is my favorite programming language, and calculate 25 * 4?"
    → Memory + Tool: calculate

    "Tell me what Python is and calculate 25 * 4."
    → Knowledge: Python + Tool: calculate

    A request may require Memory + Knowledge + Tools at the same time.

    Use all resources that are genuinely necessary, and do not request resources
    that are unnecessary.


    IMPORTANT RULES

    - Analyze the complete user message before creating the plan.
    - Select one, multiple, or zero resources depending on what the request needs.
    - Do not use Memory just because personal information exists.
    - Do not use Knowledge unless the required topic exists in Available knowledge.
    - Do not invent Memory keys, Knowledge topics, or Tools.
    - Do not answer the user.
    - Do not execute anything.
    - Keep the plan focused only on resources that are actually needed.


    Return JSON only.

    Use this structure:

    {{
    "memory": {{
    "needed": false,
            "key": null
        }},
        "knowledge": {{
    "needed": false,
            "topic": null
        }},
        "tools": {{
    "needed": false,
            "tool": null
        }}
    }}

    When a resource is not needed, set "needed" to false and its value to null.

    When a resource is needed, set "needed" to true and provide the exact
    available key, topic, or tool name.

    Do not include explanations outside the JSON.
    """

    response = chat(
        model="qwen3.5:9b",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    result = response.message.content
    result = result.replace("```json", "").replace("```", "").strip()

    print(result)

    try:
        result = json.loads(result)
    except json.JSONDecodeError:
        return {"action": "answer"}

    return result