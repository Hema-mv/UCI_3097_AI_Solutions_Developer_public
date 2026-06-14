from services.llm import ask_ollama

response = ask_ollama("List 3 reasons why customers return food products.")
print(response)