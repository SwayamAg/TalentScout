from llm_client import get_llm_response
from prompts import SYSTEM_PROMPT, TECH_QUESTION_PROMPT_TEMPLATE

EXIT_KEYWORDS = ["exit", "quit", "done", "thank you"]

def is_exit_message(user_input: str) -> bool:
    return user_input.lower().strip() in EXIT_KEYWORDS


def generate_technical_questions(tech_stack: str):
    prompt = TECH_QUESTION_PROMPT_TEMPLATE.format(tech_stack=tech_stack)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt}
    ]

    return get_llm_response(messages)


def get_greeting_message():
    return (
        "Hello! 👋 I’m TalentScout, your hiring assistant.\n\n"
        "I’ll ask you a few questions to understand your background "
        "and technical skills. Let’s get started!"
    )


def get_closing_message():
    return (
        "Thank you for your time! 🙏\n\n"
        "Your information has been recorded. "
        "Our recruitment team will review your profile and contact you regarding next steps."
    )


if __name__ == "__main__":
    print("Testing tech question generation...\n")
    result = generate_technical_questions("Python, Django")
    print(result)
