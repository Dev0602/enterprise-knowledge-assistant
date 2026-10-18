import requests


MODEL_NAME = "qwen2.5:3b"
OLLAMA_URL = "http://localhost:11434/api/generate"


def generate_answer(question: str, context: str) -> str:
    """
    Generate an answer using Qwen through Ollama.

    The model is instructed to answer only from the
    retrieved company context.
    """

    prompt = f"""You are an Enterprise Knowledge Assistant.

Answer the user's question using ONLY the company information
provided below.

COMPANY INFORMATION:
{context}

USER QUESTION:
{question}

Instructions:
- Answer the question directly.
- Use only information from the company information.
- Do not use outside knowledge.
- Do not make up facts.
- If the company information contains the answer, provide the answer.
- Keep the answer concise and clear.

ANSWER:
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0
            },
        },
        timeout=120,
    )

    response.raise_for_status()

    data = response.json()

    answer = data["response"].strip()

    print("\nGenerated answer:")
    print(answer)

    return answer