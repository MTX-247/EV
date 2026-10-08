from ollama import chat
import time


calculator_tool = {
    "type": "function",
    "function": {
        "name": "calculate",
        "description": "Calculate mathematical expressions.",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "The mathematical expression to calculate."
                }
            },
            "required": ["expression"]
        }
    }
}


def calculate(expression):
    try:
        return str(eval(expression))
    except Exception as e:
        return f"Calculation error: {e}"


available_tools = {
    "calculate": calculate
}


def execute_tool(tool_name, arguments):
    function = available_tools.get(tool_name)
    if function:
        try:
            return function(**arguments)
        except Exception as e:
            return f'\n[Error: {e}]'
    else:
        return f"Tool '{tool_name}' not found."


def think(messages):
    start = time.perf_counter()

    response = chat(
        model="qwen3.5:9b",
        messages=messages,
        tools=[calculator_tool],
        stream=False,
        options={
            "num_predict": 256,
        },
    )

    assistant_message = response.message

    # Add the assistant response to the conversation
    messages.append(assistant_message.model_dump(exclude_none=True))

    tool_iterations = 0
    MAX_TOOL_ITERATIONS = 10

    # Check if the model wants to use a tool
    while assistant_message.tool_calls and tool_iterations < MAX_TOOL_ITERATIONS:

        for tool_call in assistant_message.tool_calls:

            tool_name = tool_call.function.name
            arguments = tool_call.function.arguments
            result = execute_tool(tool_name, arguments)

            print(f"\n[Tool: {tool_name}]")
            print(f"[Arguments: {arguments}]")
            print(f"[Result: {result}]")

            messages.append({
                "role": "tool",
                "content": str(result),
                "tool_name": tool_name
            })

        # Ask the model for the final answer after receiving
        # the tool result
        final_response = chat(
            model="qwen3.5:9b",
            messages=messages,
            tools=[calculator_tool],
            options={
                "num_predict": 256,
            },
        )

        final_message = final_response.message

        assistant_message = final_message

        messages.append(
            final_message.model_dump(exclude_none=True)
        )
        tool_iterations += 1

    end = time.perf_counter()

    print(f"\n[Total: {end - start:.2f}s]")

    content = assistant_message.content
    return content