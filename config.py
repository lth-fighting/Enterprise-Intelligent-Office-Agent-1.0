from langchain.text_splitter import RecursiveCharacterTextSplitter
import streamlit as st

# DeepSeek 基址
DEEPSEEK_URL = "https://api.deepseek.com"
# DeepSeek api_key
DEEPSEEK_KEY = "sk-your-deepseek-api-key"

# 百度语音识别 api_key
BAIDU_API_KEY = "your-baidu-api-key"
# 百度语音识别密钥
BAIDU_SECRET_KEY = "your-baidu-secret-key"

# 向量嵌入模型
EMBEDDING_MODEL = "./bge-small-zh-v1.5"

# 文本分割配置
TEXT_SPLITER = RecursiveCharacterTextSplitter(
    chunk_size=400,
    chunk_overlap=100,
    length_function=len,
    separators=[r"\n\n", r"\n", "。", "！", "？", r"\nChapter", r"(?<=\. )", " ", ""]
)

# 向量数据库存储目录
CHROMA_PERSIST_DIR = './chroma_db'

# 企业数据库存储目录
DATABASE_DIR = './sqlite_set'
# 企业数据库元数据
DATABASE_METADATA = {}

# 知识库查询提示词
RAG_SYS_PROMPT = """
【角色与任务】
你是一个专业的企业文档分析助手，你需要根据用户的问题结合具体的文档上下文内容进行回答，用于提高企业对文档的阅读效率

【文档上下文内容】
{context}

【员工的问题】
{question}

【注意】
1.你需要从文档上下文内容中搜索到用户需要的信息，并经过提炼后给到企业的人员，不能回复与问题无关的内容
2.员工上传的文档内容可能不止一份，你需要综合多篇文档的内容，串联式的总结答案并回复
3.你的回答必须简洁明了、逻辑清晰，不能出现摸棱两可的情况，以提高员工的工作效率
4.在回复的最后，你可以适当地添加一些表情或问候语关心员工，能够体现企业对员工的关爱
"""

# 企业数据库查询提示词
SQLITE_SYS_PROMPT = """
【角色与任务】
你是一个专业的企业数据库查询分析师，你需要将用户的数据库查询问题依据自然语言和SQL语言的转换规则进行转换，并通过转换后的SQL语句进行数据库的查询并将查询到的结果用自然语言进行提炼，使得员工能够提高数据获取的效率

【员工的问题】
{question}
"""

# 企业会议纪要提炼提示词
MEETING_MINUTES_PROMPT = """
【角色与任务】
你是一个企业的会议要点记录师，你需要根据企业会议的内容提炼出关键的内容，并根据员工的问题依据内容生成结构化会议纪要并进行回复

【会议全部内容】
{context}

【员工的问题
{question}

【注意】
1.你要严格根据会议全部内容进行会议要点的提炼，禁止对会议内容进行无中生有的加工
2.你可以在纪要中加入一些emoji或其它标记使得会议纪要中的关键内容更加醒目
3.你的回复有简洁明了、逻辑清晰，回复的结构要美观得体
"""


# streamlit状态初始化
def init_session_status(reset=False):
    if reset:
        st.session_state.vector_db = None
        st.session_state.processed_files = {}
        st.session_state.keyword_retriever = None
        st.session_state.messages = []
        st.session_state.chat_history_store = {}
        st.session_state.messages_doc = []
        st.session_state.messages_database = []
        st.session_state.chat_history_store = {}
        st.session_state.processed_voice_files = {}
        st.session_state.meeting_history = []

    if "vector_db" not in st.session_state:
        st.session_state.vector_db = None
    if "processed_files" not in st.session_state:
        st.session_state.processed_files = {}
    if "keyword_retriever" not in st.session_state:
        st.session_state.keyword_retriever = None
    if "messages_doc" not in st.session_state:
        st.session_state.messages_doc = []
    if "messages_database" not in st.session_state:
        st.session_state.messages_database = []
    if "chat_history_store" not in st.session_state:
        st.session_state.chat_history_store = {}
    if "processed_voice_files" not in st.session_state:
        st.session_state.processed_voice_files = {}
    if "meeting_history" not in st.session_state:
        st.session_state.meeting_history = []

