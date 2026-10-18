import ollama


MODEL_NAME = "qwen2.5:3b"


def check_groundedness(
    question: str,
    answer: str,
    context: str,
) -> dict:
    """
    Check whether the answer is grounded in the retrieved context.

    Three possible outcomes:

    SUPPORTED
        The answer's factual claims are supported by the context.

    ABSTENTION
        The assistant correctly says that the information
        cannot be found in the knowledge base.

    NOT_SUPPORTED
        The answer contains factual claims that are not
        supported by the context.
    """

    # ---------------------------------------------------------
    # 1. Deterministic check for correct abstention
    # ---------------------------------------------------------

    abstention_phrases = [
        "i couldn't find that information",
        "i could not find that information",
        "not available in the company knowledge base",
        "not found in the company knowledge base",
        "does not include",
        "do not include",
        "doesn't include",
        "cannot find that information",
    ]

    answer_lower = answer.lower()

    if any(
        phrase in answer_lower
        for phrase in abstention_phrases
    ):
        return {
            "verdict": "ABSTENTION",
            "reason": (
                "VERDICT: ABSTENTION\n"
                "REASON: The assistant correctly states that "
                "the requested information is not available "
                "in the company knowledge base."
            ),
        }

    # ---------------------------------------------------------
    # 2. Ask Qwen to evaluate factual support
    # ---------------------------------------------------------

    prompt = f"""
You are a strict but fair evaluator for an Enterprise
Knowledge Assistant.

Your ONLY task is to determine whether the factual claims
in the ANSWER are supported by the COMPANY INFORMATION.

IMPORTANT:

Do NOT judge whether the answer perfectly answers the
user's personal situation.

Do NOT require the answer to contain additional information
that was not asked for.

Do NOT use outside knowledge.

If the answer paraphrases the company information,
that is SUPPORTED.

For example:

COMPANY INFORMATION:
Employees may work remotely when their role, manager
approval, and business needs allow it.

ANSWER:
Eligibility for remote work depends on the employee's role,
manager approval, and business needs.

This is SUPPORTED because the answer expresses the same
information in different words.

Use exactly one of these verdicts:

SUPPORTED
The factual claims in the answer are supported by the
company information.

NOT_SUPPORTED
The answer contains factual claims that contradict or
go beyond the company information.

COMPANY INFORMATION:
{context}

USER QUESTION:
{question}

ANSWER:
{answer}

Return exactly:

VERDICT: SUPPORTED
REASON: The factual claims in the answer are supported
by the company information.

OR:

VERDICT: NOT_SUPPORTED
REASON: The answer contains factual claims that are not
supported by the company information.
"""

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
    )

    result = response["message"]["content"].strip()

    # ---------------------------------------------------------
    # 3. Parse evaluator result
    # ---------------------------------------------------------

    if "VERDICT: SUPPORTED" in result:
        verdict = "SUPPORTED"

    elif "VERDICT: NOT_SUPPORTED" in result:
        verdict = "NOT_SUPPORTED"

    else:
        verdict = "NOT_SUPPORTED"

    return {
        "verdict": verdict,
        "reason": result,
    }