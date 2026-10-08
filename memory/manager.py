import json

class MemoryManager:
    def __init__(self):
        pass

    def load_history(self):
        with open("memory/memory.json", "r") as file:
            messages = json.load(file)
            return messages

    def save_history(self, messages):
        with open("memory/memory.json", "w") as file:
            json.dump(messages, file)

    def remember(self, key, value):
        with open("memory/facts.json", "r") as file:
            facts = json.load(file)

        facts[key] = value

        with open("memory/facts.json", "w") as file:
            json.dump(facts, file, indent=4)

    def recall(self, key):
        with open("memory/facts.json", "r") as file:
            facts = json.load(file)
            return facts.get(key)

    def get_all_facts(self):
        with open("memory/facts.json", "r") as file:
            facts = json.load(file)
            return facts
    def forget(self, key):
        with open("memory/facts.json", "r") as file:
            json_facts = json.load(file)
            del json_facts[key]
            with open("memory/facts.json", "w") as file:
                json.dump(json_facts, file)



