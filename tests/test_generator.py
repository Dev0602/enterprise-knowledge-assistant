from src.generation.generator import generate_answer


question = "Can I work remotely?"

context = """
Enterprise Remote Work Policy

Employees may work remotely when their role,
manager approval, and business needs allow it.
Some roles may require regular on-site work.

Employees should be available during their team's
agreed core hours.
"""


answer = generate_answer(
    question=question,
    context=context,
)

print("\nQUESTION:")
print(question)

print("\nANSWER:")
print(answer)