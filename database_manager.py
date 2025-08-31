# database_manager.py
import os.path
import sqlite3
from config import DATABASE_DIR, DATABASE_METADATA
import streamlit as st
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import AgentType
from deepseek_llm import llm


class DatabaseManager:
    def __init__(self):
        self.databases = {}
        self.db_descriptions = {}
        self.load_databases()

    def load_databases(self):
        if not os.path.exists(DATABASE_DIR):
            os.makedirs(DATABASE_DIR)
            st.warning(f"路径 {DATABASE_DIR} 不存在，已为你创建新目录")
            return

        db_files = [f for f in os.listdir(DATABASE_DIR) if f.endswith('.db')]

        for db_file in db_files:
            db_path = os.path.join(DATABASE_DIR, db_file)
            db_name = os.path.splitext(db_file)[0]

            try:
                db = SQLDatabase.from_uri(
                    f"sqlite:///{db_path}",
                    sample_rows_in_table_info=2
                )

                metadata = self.extract_database_metadata(db, db_path)

                self.databases[db_name] = db
                self.db_descriptions[db_name] = metadata

                DATABASE_METADATA[db_name] = metadata
            except Exception as e:
                st.error(f"加载数据库 {db_name} 时出现错误: {str(e)}")

    def extract_database_metadata(self, db, db_path):
        """
        提取数据库表结构和描述性信息
        :param db: 数据库名
        :param db_path: 数据库路径
        :return: 返回数据库元数据
        """
        metadata = {
            "path": db_path,
            "tables": {},
            "description": f"数据库文件: {os.path.basename(db_path)}"
        }

        try:
            table_names = db.get_usable_table_names()

            for table_name in table_names:
                table_info = db.get_table_info([table_name])

                with sqlite3.connect(db_path) as conn:
                    cursor = conn.cursor()
                    cursor.execute(f"SELECT * FROM {table_name} LIMIT 1")
                    columns = [description[0] for description in cursor.description]

                metadata["tables"][table_name] = {
                    "columns": columns,
                    "sample_data": table_info
                }

            database_description_prompt = f"""
            【角色与任务】
            你是一个数据库描述助手，你需要用一句话描述以下数据库的用途和主要内容，用于帮助选择最相关的数据库进行数据的查询
            
            【数据库文件名】
            {os.path.basename(db_path)}
            
            【数据库包含的表】
            {','.join(table_names)}
            
            【注意】
            你只需要回复数据库的描述即可，禁止回复与数据库描述无关的内容
            """

            try:
                description = llm.invoke(database_description_prompt).content
                if description:
                    metadata["description"] = description
            except Exception as e:
                metadata["description"] = f"包含 {len(table_names)} 个表的数据库: {','.join(table_names)}, 默认描述原因: {str(e)}"

        except Exception as e:
            st.error(f"提取数据库表结构时出错: {str(e)}")

        return metadata

    def select_database(self, query: str):
        if not self.databases:
            return None, "没有可用的数据库"

        if len(self.databases) == 1:
            db_name = list(self.databases.keys())[0]
            return self.databases[db_name], f"使用数据库: {db_name}"

        db_options = "\n".join([
            f"{i+1}. {name}: {self.db_descriptions[name]["description"]}"
            for i, name in enumerate(self.databases.keys())
        ])

        select_database_prompt = f"""
        【角色与任务】
        你是一个专业的企业数据库使用决策师，你需要根据员工提出的问题选择最相关的数据库，并返回数据库名称
        
        【员工问题】
        {query}
        
        【可用数据库】
        {db_options}
        
        【注意】
        1.你只需要返回该数据库的名称即可，禁止返回其它信息
        2.你只能从可用的数据库中选择合适的数据库并返回该数据库的名称，禁止返回没有出现在可用数据库中的数据库名
        """

        try:
            db_name = llm.invoke(select_database_prompt).content.strip()
            return self.databases[db_name]

        except Exception as e:
            st.error(f"选择数据库时出错: {str(e)}")
            db_name = list(self.databases.keys())[0]
            return self.databases[db_name], f"已选择数据库: {db_name} (默认)"

    def get_database_list(self):
        """获取数据库列表用于显示"""
        return [
            {"name": name, "description": self.db_descriptions[name]["description"]}
            for name in self.databases.keys()
        ]


db_manager = DatabaseManager()
