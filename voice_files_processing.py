import tempfile
from voice_manager import file_to_txt
import streamlit as st
import os


def process_audio(voice_files):
    meeting_content = ""

    for i, file in enumerate(voice_files):
        if file.name in st.session_state.processed_voice_files:
            st.info(f"文件 {file.name} 已处理过，跳过")
            continue

        with st.spinner(f"正在处理 {file.name}..."):
            with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file.name.split('.')[-1]}") as tmp_file:
                tmp_file.write(file.getvalue())
                tmp_file_path = tmp_file.name

            try:
                detect_result = file_to_txt(tmp_file_path)

                if detect_result and detect_result != "未识别到有效语音内容":
                    st.success(f"音频 {file.name} 识别成功")
                    # 将每个文件的内容追加，并注明来自哪个文件
                    meeting_content += f"\n\n--- {file.name} ---\n{detect_result}"
                    st.session_state.processed_voice_files[file.name] = True
                else:
                    st.warning(f"音频 {file.name} 识别失败或未识别到内容")
            except Exception as e:
                st.error(f"处理音频文件时出错: {str(e)}")
            finally:
                try:
                    os.unlink(tmp_file_path)
                except:
                    pass

    return meeting_content if meeting_content else None
