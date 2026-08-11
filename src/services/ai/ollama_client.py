import requests


class OllamaClient:

    URL = "http://localhost:11434/api/chat"

    def generate(self, system_prompt, user_prompt):

        response = requests.post(
            self.URL,
            json={
                "model": "llama3.2",
                "messages": [
                    {
                        "role": "system",
                        "content": system_prompt
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ],
                "stream": False,
                "options": {
                    "temperature": 0
                }
            }
        )

        response.raise_for_status()

        return response.json()["message"]["content"]