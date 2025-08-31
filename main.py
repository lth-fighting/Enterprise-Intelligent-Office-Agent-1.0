from langchain_community.agent_toolkits import (
    create_sql_agent,
    SQLDatabaseToolkit
)
from langchain.agents import AgentType
from documents_processing import *
from retrieval_qa import get_answer
from deepseek_llm import llm
from database_manager import db_manager
from voice_manager import voice_to_txt
from voice_files_processing import process_audio

st.set_page_config("企业智能办公系统", page_icon="🧠", layout="wide")
init_session_status()

function = st.sidebar.selectbox("选择你需要的企业助手功能", ("企业官方文档分析", "企业数据仓库查询", "企业会议纪要总结"))

if function == "企业官方文档分析":
    st.title("📁 知识库管理")
    st.markdown("上传企业文档后即可进行分析")

    upload_files = st.sidebar.file_uploader(
        "文档仓库: 支持pdf/docx/txt...",
        type=["pdf", "docx", "txt"],
        accept_multiple_files=True
    )

    if upload_files:
        files_to_process = [f for f in upload_files if f.name not in st.session_state.processed_files]

        if files_to_process:
            with st.sidebar:
                with st.spinner("正在处理相关文档，请稍后..."):
                    result = process_documents(files_to_process)

                    if result is None:
                        st.error("文档处理失败，请重新上传")
                    else:
                        vector_db, keyword_retriever = result
                        st.session_state.vector_db = vector_db
                        st.session_state.keyword_retriever = keyword_retriever
                        st.success(f"成功处理 {len(files_to_process)} 个文档")

    for i, message in enumerate(st.session_state.messages_doc):
        if i % 2 == 0:
            with st.chat_message("user"):
                st.markdown(message["content"])
        else:
            with st.chat_message("assistant"):
                st.markdown(message["content"])

    if question := st.chat_input("你想要获取什么文档信息呢？"):
        with st.chat_message("user"):
            st.markdown(question)

        with st.spinner("正在问您翻阅文档，请稍后..."):
            answer, docs = get_answer(question)

        st.session_state.messages_doc.append({"role": "user", "content": question})
        st.session_state.messages_doc.append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):
            st.markdown(answer)

    voice_chick = st.button("🎤", help="点击开始语音输入")

    if voice_chick:
        voice_input = voice_to_txt()
        if voice_input == "未识别到有效语音内容":
            st.warning(voice_input)
        else:
            with st.chat_message("user"):
                st.markdown(voice_input)

            with st.spinner("正在问您翻阅文档，请稍后..."):
                answer, docs = get_answer(voice_input)

            st.session_state.messages_doc.append({"role": "user", "content": voice_input})
            st.session_state.messages_doc.append({"role": "assistant", "content": answer})
            with st.chat_message("assistant"):
                st.markdown(answer)

if function == "企业数据库查询":
    st.title("🗃️ 企业数据库")

    db_files = [db for db in os.listdir('./sqlite_set') if db.endswith('.db')]
    with st.sidebar:
        st.header("企业数据仓库")
        databases = db_manager.get_database_list()

        if not databases:
            st.warning("没有找到数据库文件，请将.db文件放入./sqlite_set/ 目录中")
        else:
            for i, db in enumerate(databases):
                st.sidebar.write(f"{i + 1}. {db['name']}")
                st.sidebar.caption(f"   {db['description']}")

        selected_db = st.sidebar.selectbox(
            "选择要查询的数据库",
            options=[db["name"] for db in databases] if databases else ["无可用数据库"],
            index=0
        )

    question = st.chat_input("你想查询的企业数据是什么呢？")

    for i, message in enumerate(st.session_state.messages_database):
        if i % 2 == 0:
            with st.chat_message("user"):
                st.markdown(message["content"])
        else:
            with st.chat_message("assistant"):
                st.markdown(message["content"]["output"])

    if question:
        with st.chat_message("user"):
            st.markdown(question)

        if selected_db and selected_db != "无可用数据库":
            db = db_manager.databases[selected_db]
            db_info = f"已手动选择数据库: {selected_db}"
        else:
            db, db_info = db_manager.select_database(question)

            # 显示数据库选择信息
        st.info(db_info)

        try:
            # 创建SQL Agent
            toolkit = SQLDatabaseToolkit(db=db, llm=llm)

            agent_executor = create_sql_agent(
                llm=llm,
                toolkit=toolkit,
                agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                verbose=True,
                top_k=3,
                handle_parsing_errors=True
            )

            # 执行查询
            answer = agent_executor.invoke({"input": question})

            # 保存到聊天历史
            st.session_state.messages_database.append({"role": "user", "content": question})
            st.session_state.messages_database.append({"role": "assistant", "content": answer})

            # 显示结果
            with st.chat_message("assistant"):
                st.markdown(answer['output'])

        except Exception as e:
            error_msg = f"查询数据库时出错: {str(e)}"
            st.error(error_msg)
            st.session_state.messages_database.append({"role": "user", "content": question})
            st.session_state.messages_database.append({"role": "assistant", "content": {"output": error_msg}})

    voice_chick = st.button("🎤", help="点击开始语音输入")

    if voice_chick:
        voice_input = voice_to_txt()
        if voice_input == "未识别到有效语音内容":
            st.warning(voice_input)

        else:
            with st.chat_message("user"):
                st.markdown(voice_input)

            if selected_db and selected_db != "无可用数据库":
                db = db_manager.databases[selected_db]
                db_info = f"已手动选择数据库: {selected_db}"
            else:
                db, db_info = db_manager.select_database(voice_input)

                # 显示数据库选择信息
            st.info(db_info)

            try:
                # 创建SQL Agent
                toolkit = SQLDatabaseToolkit(db=db, llm=llm)

                agent_executor = create_sql_agent(
                    llm=llm,
                    toolkit=toolkit,
                    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                    verbose=True,
                    top_k=3,
                    handle_parsing_errors=True
                )

                # 执行查询
                answer = agent_executor.invoke({"input": voice_input})

                # 保存到聊天历史
                st.session_state.messages_database.append({"role": "user", "content": voice_input})
                st.session_state.messages_database.append({"role": "assistant", "content": answer})

                # 显示结果
                with st.chat_message("assistant"):
                    st.markdown(answer['output'])

            except Exception as e:
                error_msg = f"查询数据库时出错: {str(e)}"
                st.error(error_msg)
                st.session_state.messages_database.append({"role": "user", "content": voice_input})
                st.session_state.messages_database.append({"role": "assistant", "content": {"output": error_msg}})

if function == "企业会议纪要总结":
    st.title("💻 会议纪要总结")
    st.caption("上传音频文件后即可进行音频总结")

    voice_files = st.sidebar.file_uploader(
        "选择或拖放音频文件",
        type=["wav"],
        accept_multiple_files=True
    )

    # 初始化会议内容
    if "meeting_content" not in st.session_state:
        st.session_state.meeting_content = ""

    if voice_files:
        # 处理新上传的文件
        new_content = process_audio(voice_files)
        if new_content:
            # 将新内容追加到现有的会议内容中
            st.session_state.meeting_content += new_content
            with st.expander("查看音频识别内容"):
                st.text(st.session_state.meeting_content)
        else:
            st.warning("没有从音频中识别到内容")

    if st.session_state.meeting_content:
        with st.expander("查看已识别的会议内容"):
            st.text(st.session_state.meeting_content)

    for i, message in enumerate(st.session_state.meeting_history):
        if i % 2 == 0:
            with st.chat_message("user"):
                st.markdown(message["content"])
        else:
            with st.chat_message("assistant"):
                st.markdown(message["content"])

    if question := st.chat_input("你想获取会议中的什么信息呢？"):
        # 确保会议内容不为空
        if not st.session_state.meeting_content:
            st.warning("请先上传并处理音频文件")
        else:
            with st.chat_message("user"):
                st.markdown(question)

            prompt_text = f"{MEETING_MINUTES_PROMPT.format(
                context=st.session_state.meeting_content, 
                question=question
            )}"

            with st.spinner("正在生成会议纪要..."):
                try:
                    answer = llm.invoke(prompt_text).content

                    with st.chat_message("assistant"):
                        st.markdown(answer)

                    st.session_state.meeting_history.append({"role": "user", "content": question})
                    st.session_state.meeting_history.append({"role": "assistant", "content": answer})

                except Exception as e:
                    st.error(f"生成会议纪要时出错: {str(e)}")
