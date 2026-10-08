import json

def save_knowledge(result):
    with open("memory/knowledge/knowledge.json", "r") as file:
        data = json.load(file)
        if result["learn"] == True:
            data[result["topic"]] = result["knowledge"]
            with open("memory/knowledge/knowledge.json", "w") as file:
                json.dump(data, file)

def load_knowledge():
    with open("memory/knowledge/knowledge.json", "r") as file:
        data = json.load(file)
        return data
