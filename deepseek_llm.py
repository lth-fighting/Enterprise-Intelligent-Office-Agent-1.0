from config import *
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    openai_api_key=DEEPSEEK_KEY,
    openai_api_base=DEEPSEEK_URL,
    model_name='deepseek-chat',
    temperature=0.5
)


def documents_answer(prompt):
    try:
        res = llm.invoke(prompt)
        return res.content
    except Exception as e:
        return f"调用DeepSeek API时出错: {str(e)}"


def database_answer(prompt):
    try:
        res = llm.invoke(prompt)
        return res.content
    except Exception as e:
        return f"调用DeepSeek API时出错: {str(e)}"
