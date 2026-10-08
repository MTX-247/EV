from memory.manager import MemoryManager
from core.memory_agent import extract_memory, find_memory, find_forget_memory
from core.learner import learn
from core.knowledge import save_knowledge, load_knowledge
from core.brain import think
from core.planner import plan


memory = MemoryManager()
messages = memory.load_history()


while True:
    user_input = input("Ahmed: ")
    
    if user_input.lower() in ["exit", "quit"]:
        break

    facts = memory.get_all_facts()

    knowledge = load_knowledge()
    knowledge_topics = list(knowledge.keys())

    plan_data = plan(user_input, facts, knowledge_topics)

    print(f"[Planner] {plan_data}")

    forget_data = find_forget_memory(user_input, facts)

    if forget_data.get("forget"):
        memory.forget(forget_data["key"])
        facts = memory.get_all_facts()



    recall_data = find_memory(user_input, facts)
    print(f"[Memory Recall] {recall_data}")

    current_messages = messages.copy()

    if plan_data.get("action") == "knowledge":
        topic = plan_data["topic"]
        knowledge_text = knowledge.get(topic)

        if knowledge_text:
            current_messages.append({
                "role": "system",
                "content": f"Relevant knowledge: {topic} = {knowledge_text}"
            })

    if recall_data.get("recall"):
        key = recall_data["key"]
        value = memory.recall(key)

        current_messages.append({
            "role": "system",
            "content": f"Relevant memory about Ahmed: {key} = {value}"
        })

    current_messages.append({
        "role": "user",
        "content": user_input
    })

    memory_keywords = [
        "my",
        "i am",
        "i'm",
        "i like",
        "i love",
        "i hate",
        "my favorite",
        "i prefer",
        "i want",
        "i use",
        "i have",
    ]

    should_check_memory = any(
        keyword in user_input.lower()
        for keyword in memory_keywords
    )

    if should_check_memory:
        memory_data = extract_memory(user_input, facts)

        if memory_data.get("remember"):
            memory.remember(
                memory_data["key"],
                memory_data["value"]
            )

    response = think(current_messages)

    result = learn(user_input)
    if result.get("learn"):
        save_knowledge(result)

    print(f"E.V: {response}")

    messages = current_messages

    memory.save_history(messages)