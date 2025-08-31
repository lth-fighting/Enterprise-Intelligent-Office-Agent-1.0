# 🧠 企业智能办公系统

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io/)
[![LangChain](https://img.shields.io/badge/LangChain-00C2FF?style=for-the-badge)](https://www.langchain.com/)
[![DeepSeek](https://img.shields.io/badge/DeepSeek-LLM-blue?style=for-the-badge)](https://deepseek.com/)
[![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org)

一个基于大语言模型（LLM）的企业级智能办公助手系统，支持文档分析、数据库查询、会议语音转写与总结等功能，提升企业信息处理与员工协作效率。

---

## 📋 目录

1. [项目概述](#-项目概述)
2. [功能特性](#-功能特性)
3. [技术架构](#-技术架构)
4. [安装部署](#-安装部署)
   - [环境要求](#环境要求)
   - [克隆项目](#1-克隆项目)
   - [安装依赖](#2-安装依赖)
   - [下载Embedding模型](#3-下载embedding模型)
   - [配置API密钥](#4-配置api密钥)
   - [准备数据库](#5-准备数据库可选)
   - [运行系统](#6-运行系统)
5. [配置文件详解](#-配置文件详解)
6. [项目结构详解](#-项目结构详解)
7. [核心模块说明](#-核心模块说明)
   - [文档处理模块](#1-文档处理模块)
   - [数据库管理模块](#2-数据库管理模块)
   - [语音处理模块](#3-语音处理模块)
   - [检索与问答模块](#4-检索与问答模块)
   - [DeepSeek集成模块](#5-deepseek集成模块)
8. [使用指南](#-使用指南)
   - [文档分析功能](#1-文档分析功能)
   - [数据库查询功能](#2-数据库查询功能)
   - [会议纪要功能](#3-会议纪要功能)
9. [API接口说明](#-api接口说明)
10. [常见问题解答](#-常见问题解答)
11. [性能优化建议](#-性能优化建议)
12. [开发计划](#-开发计划)
13. [贡献指南](#-贡献指南)
14. [许可证](#-许可证)
15. [联系方式](#-联系方式)

---

## 🏢 项目概述

企业智能办公系统是一个集成了现代AI技术的企业级应用，旨在帮助企业更高效地处理文档、查询数据和总结会议内容。系统结合了大型语言模型、向量数据库和语音识别技术，提供了直观的Web界面，使非技术用户也能轻松使用高级AI功能。

### 设计理念
- **用户友好**: 基于Streamlit的直观界面，降低使用门槛
- **模块化设计**: 各功能模块独立，便于维护和扩展
- **企业级安全**: 支持本地部署，保护企业数据隐私
- **多模态输入**: 支持文本、语音和文件多种输入方式

### 适用场景
- 企业知识库管理与查询
- 业务数据探索与分析
- 会议记录与内容总结
- 员工自助服务与信息检索

---

## ✨ 功能特性

### 📁 企业官方文档分析
- 支持上传PDF、DOCX、TXT等多种格式文档
- 自动文档解析与内容提取
- 基于向量检索与关键词检索的混合检索机制
- 多文档联合查询与答案生成
- 文档来源追踪与引用显示

### 🗃️ 企业数据仓库查询
- 多SQLite数据库动态加载与元数据提取
- 自然语言转SQL查询，支持复杂查询条件
- 可视化数据库结构与查询结果
- 语音输入支持，方便移动端使用
- 智能数据库选择与错误处理

### 💻 会议纪要总结
- WAV格式音频文件上传与处理
- 高精度语音识别转文字
- 多文件拼接与上下文关联
- 结构化会议纪要生成
- 关键信息提取与标记

### 🎤 语音交互支持
- 集成百度语音识别API，支持实时语音输入
- 音频文件批量处理与识别
- 语音指令响应与反馈
- 离线语音识别支持（需额外配置）

---

## 🏗️ 技术架构

### 系统架构图
```
企业智能办公系统
├── 前端界面 (Streamlit)
├── 业务逻辑层
│   ├── 文档处理模块
│   ├── 数据库管理模块
│   ├── 语音处理模块
│   └── 问答生成模块
├── AI服务层
│   ├── DeepSeek LLM
│   ├── BGE嵌入模型
│   └── 百度语音识别
└── 数据存储层
    ├── 向量数据库 (Chroma)
    └── 关系数据库 (SQLite)
```

### 技术选型理由
- **Streamlit**: 快速构建数据应用，适合AI原型开发
- **LangChain**: 提供LLM应用开发框架，简化复杂流程
- **ChromaDB**: 轻量级向量数据库，适合嵌入应用
- **BGE模型**: 中文优化嵌入模型，适合企业文档处理
- **DeepSeek**: 性价比高的中文LLM服务，API稳定

---

## 📦 安装部署

### 环境要求

- Python 3.8+
- CUDA 11.7+（如需GPU推理）
- Git
- 至少8GB内存（处理大型文档时需要更多）
- 至少10GB磁盘空间（用于模型和数据库存储）

### 1. 克隆项目

```bash
git clone https://github.com/lth-fighting/Enterprise-Intelligent-Office-Agent-1.0.git
cd your-repo-name
```

### 2. 安装依赖

```bash
# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装依赖包
pip install -r requirements.txt

# 如遇网络问题，可使用国内镜像
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 3. 下载Embedding模型

由于 `bge-small-zh-v1.5` 模型较大（约1.2GB），请从Hugging Face下载：

```bash
# 使用git lfs（推荐）
git lfs install
git clone https://huggingface.co/BAAI/bge-small-zh-v1.5

# 或手动下载
# 1. 访问 https://huggingface.co/BAAI/bge-small-zh-v1.5
# 2. 下载所有文件到项目根目录下的 bge-small-zh-v1.5 文件夹
# 3. 确保文件结构如下：
#    bge-small-zh-v1.5/
#    ├── config.json
#    ├── pytorch_model.bin
#    ├── special_tokens_map.json
#    ├── tokenizer.json
#    ├── tokenizer_config.json
#    └── vocab.txt
```

### 4. 配置API密钥

在 `config.py` 中配置以下密钥：

```python
# DeepSeek API配置
DEEPSEEK_URL = "https://api.deepseek.com"
DEEPSEEK_KEY = "sk-your-deepseek-api-key-here"  # 替换为你的实际密钥

# 百度语音识别API配置
BAIDU_API_KEY = "your-baidu-api-key-here"       # 替换为你的实际密钥
BAIDU_SECRET_KEY = "your-baidu-secret-key-here" # 替换为你的实际密钥
```

#### 如何获取API密钥

**DeepSeek API密钥**:
1. 访问 [DeepSeek官网](https://www.deepseek.com/)
2. 注册账号并登录
3. 进入API管理页面创建新密钥
4. 复制密钥到配置文件中

**百度语音识别密钥**:
1. 访问 [百度智能云](https://cloud.baidu.com/)
2. 注册账号并登录
3. 进入「语音技术」服务页面
4. 创建应用并获取API Key和Secret Key

### 5. 准备数据库（可选）

将SQLite数据库文件（`.db`）放入 `./sqlite_set/` 目录，系统会自动加载。

可以使用提供的 `sqlite.py` 脚本创建示例数据库：

```bash
# 创建示例企业数据库
python sqlite.py
```

这将创建一个包含企业基本数据的SQLite数据库文件。

### 6. 运行系统

在项目目录下终端运行启动命令：

```bash
streamlit run main.py
```

访问提示的本地URL（默认为 `http://localhost:8501`）即可使用。

#### 高级运行选项

```bash
# 指定端口运行
streamlit run main.py --server.port 8502

# 启用调试模式
streamlit run main.py --logger.level debug

# 使用GPU加速（如果可用）
CUDA_VISIBLE_DEVICES=0 streamlit run main.py
```

---

## ⚙️ 配置文件详解

### config.py 完整配置说明

```python
# 文本分割配置
TEXT_SPLITER = RecursiveCharacterTextSplitter(
    chunk_size=400,           # 文本块大小
    chunk_overlap=100,        # 文本块重叠大小
    length_function=len,      # 长度计算函数
    separators=[r"\n\n", r"\n", "。", "！", "？", r"\nChapter", r"(?<=\. )", " ", ""]  # 分割符
)

# 向量数据库配置
CHROMA_PERSIST_DIR = './chroma_db'  # 向量数据库存储路径

# 企业数据库配置
DATABASE_DIR = './sqlite_set'      # 数据库文件存放目录
DATABASE_METADATA = {}             # 数据库元数据缓存

# 知识库查询提示词模板
RAG_SYS_PROMPT = """
【角色与任务】
你是一个专业的企业文档分析助手，你需要根据用户的问题结合具体的文档上下文内容进行回答...

【文档上下文内容】
{context}

【员工的问题】
{question}

【注意】
1.你需要从文档上下文内容中搜索到用户需要的信息...
"""
```

### 自定义配置建议

1. **调整文本分块参数**: 根据文档类型调整chunk_size和chunk_overlap
2. **修改向量数据库路径**: 如果需要多版本管理，可动态设置CHROMA_PERSIST_DIR
3. **定制提示词模板**: 根据企业特定需求修改各功能的提示词模板

---

## 🗂️ 项目结构详解

```
企业智能办公系统/
├── main.py                     	# 主入口文件，Streamlit应用界面
├── config.py                   	# 配置文件，包含所有系统设置和API密钥
├── requirements.txt            	# Python依赖包列表
├── README.md                   	# 项目说明文档
├── 模型文件/
│   └── bge-small-zh-v1.5/      	# BGE嵌入模型（需单独下载）
├── 数据存储/
│   ├── chroma_db/              	# 向量数据库存储目录（自动生成）
│   └── sqlite_set/             	# 企业数据库存储目录（需手动创建）
├── 核心模块/
│   ├── deepseek_llm.py         	# DeepSeek LLM调用封装
│   ├── documents_processing.py 	# 文档处理与向量化模块
│   ├── retrieval_qa.py         	# 检索与问答模块
│   ├── database_manager.py     	# 数据库管理模块
│   ├── voice_manager.py        	# 语音识别模块
│   └── voice_files_processing.py 	# 音频文件处理模块
└── sqlite.py/						# 添加SQLite数据库实例
```

### 文件详细说明

1. **main.py**: 主应用文件，包含Streamlit界面和主要业务流程
2. **config.py**: 系统配置中心，包含API密钥、模型路径和提示词模板
3. **deepseek_llm.py**: 封装DeepSeek API调用，提供统一的LLM接口
4. **documents_processing.py**: 处理上传文档，包括加载、分割和向量化
5. **retrieval_qa.py**: 实现混合检索（向量+关键词）和答案生成
6. **database_manager.py**: 管理SQLite数据库，提供自然语言到SQL的转换
7. **voice_manager.py**: 语音识别功能，支持实时语音和音频文件处理
8. **voice_files_processing.py**: 处理上传的音频文件，调用语音识别
9. **sqlite.py**: 添加SQLite数据库实例，用于演示使用

---

## 🔧 核心模块说明

### 1. 文档处理模块

**文件**: `documents_processing.py`

#### 功能概述
负责处理用户上传的各种格式文档，将其转换为向量数据库可存储的格式。

#### 核心类与方法
- `load_documents(file)`: 根据文件类型选择合适的加载器
- `process_documents(files)`: 主处理流程，包括文档加载、分割和向量化

#### 支持格式
- PDF: 使用PyPDFLoader
- DOCX: 使用Docx2txtLoader
- TXT: 使用TextLoader
- 其他格式: 使用UnstructuredFileLoader

#### 处理流程
1. 文件类型检测与临时存储
2. 使用合适加载器提取文本内容
3. 文本分割为适当大小的块
4. 生成文本嵌入向量
5. 存储到Chroma向量数据库

### 2. 数据库管理模块

**文件**: `database_manager.py`

#### 功能概述
管理企业SQLite数据库，提供自然语言到SQL查询的转换功能。

#### 核心类
- `DatabaseManager`: 主管理类，负责数据库加载和查询

#### 主要方法
- `__init__()`: 初始化并加载所有可用数据库
- `load_databases()`: 从指定目录加载SQLite数据库
- `extract_database_metadata()`: 提取数据库元数据
- `select_database()`: 根据查询选择最相关数据库

#### 数据库元数据结构
```python
{
    "path": "数据库路径",
    "tables": {
        "表名": {
            "columns": ["列1", "列2", ...],
            "sample_data": "示例数据"
        }
    },
    "description": "数据库描述"
}
```

### 3. 语音处理模块

**文件**: `voice_manager.py` 和 `voice_files_processing.py`

#### 功能概述
提供语音识别功能，支持实时语音输入和音频文件处理。

#### 核心类
- `VoiceCommandSystem`: 语音命令系统主类

#### 主要方法
- `_get_baidu_token()`: 获取百度语音识别令牌
- `_recognize_baidu()`: 调用百度API进行语音识别
- `listen_for_command()`: 监听语音输入
- `process_audio_file()`: 处理音频文件

#### 音频格式支持
- 实时语音输入: 16kHz, 16位, 单声道PCM
- 音频文件: WAV格式

### 4. 检索与问答模块

**文件**: `retrieval_qa.py`

#### 功能概述
实现混合检索机制（向量+关键词）和基于上下文的问答生成。

#### 核心方法
- `hybrid_retrieval()`: 混合检索实现
- `get_answer()`: 生成答案主方法

#### 检索流程
1. 向量检索: 使用ChromaDB进行语义相似度检索
2. 关键词检索: 使用BM25算法进行关键词匹配
3. 结果合并与去重: 合并两种检索结果并去除重复
4. 上下文构建: 构建LLM所需的上下文提示
5. 答案生成: 调用DeepSeek LLM生成最终答案

### 5. DeepSeek集成模块

**文件**: `deepseek_llm.py`

#### 功能概述
封装DeepSeek LLM API调用，提供统一的语言模型接口。

#### 核心组件
- `llm`: ChatOpenAI实例，配置为使用DeepSeek API
- `documents_answer()`: 文档问答专用接口
- `database_answer()`: 数据库问答专用接口

#### API调用配置
```python
llm = ChatOpenAI(
    openai_api_key=DEEPSEEK_KEY,
    openai_api_base=DEEPSEEK_URL,
    model_name='deepseek-chat',
    temperature=0.5  # 控制生成创造性
)
```

---

## 📖 使用指南

### 1. 文档分析功能

#### 上传文档
1. 在侧边栏选择「企业官方文档分析」功能
2. 点击「文档仓库」上传按钮
3. 选择PDF、DOCX或TXT格式的文档
4. 等待文档处理完成（进度条显示）

#### 提问与查询
1. 在聊天输入框中输入问题
2. 或点击麦克风按钮进行语音输入
3. 系统会自动检索相关文档并生成答案
4. 答案下方会显示参考的文档来源

#### 示例问题
- "公司的年假政策是怎样的？"
- "财务报销流程有哪些步骤？"
- "项目管理制度中有哪些关键点？"

### 2. 数据库查询功能

#### 准备数据库
1. 将SQLite数据库文件(.db)放入`./sqlite_set/`目录
2. 系统会自动加载并分析数据库结构

#### 执行查询
1. 在侧边栏选择「企业数据仓库查询」功能
2. 从下拉菜单中选择要查询的数据库
3. 在聊天输入框中输入自然语言查询
4. 或使用语音输入查询条件

#### 示例查询
- "销售部有多少员工？"
- "显示上个月订单金额大于10000的所有客户"
- "查询张三的联系方式和部门"

### 3. 会议纪要功能

#### 上传音频
1. 在侧边栏选择「企业会议纪要总结」功能
2. 点击「选择或拖放音频文件」上传WAV格式音频
3. 等待语音识别完成（可查看识别结果）

#### 会议内容查询
1. 在聊天输入框中输入关于会议内容的问题
2. 系统会基于会议转录文本生成回答
3. 可以请求生成结构化会议纪要

#### 示例请求
- "会议讨论了哪些产品计划？"
- "生成结构化会议纪要"
- "有哪些关键决策和行动项？"

---

## 🌐 API接口说明

### DeepSeek API接口

#### 请求示例
```python
from deepseek_llm import llm

response = llm.invoke("你的问题或提示")
answer = response.content
```

#### 参数说明
- `temperature`: 控制生成创造性（0.0-1.0）
- `max_tokens`: 生成的最大令牌数
- `top_p`: 核采样概率阈值

### 百度语音识别API

#### 初始化示例
```python
from voice_manager import VoiceCommandSystem

voice_system = VoiceCommandSystem(
    baidu_api_key=YOUR_API_KEY,
    baidu_secret_key=YOUR_SECRET_KEY
)
```

#### 音频格式要求
- 采样率: 16000Hz
- 位深度: 16位
- 声道数: 单声道
- 编码: PCM

---

## ❓ 常见问题解答

### Q: 模型下载失败或速度慢怎么办？
A: 可以尝试以下方法：
1. 使用Hugging Face镜像站：`HF_ENDPOINT=https://hf-mirror.com`
2. 手动下载后放置到对应目录
3. 使用代理或VPN加速下载

### Q: 语音识别准确率不高怎么办？
A: 可以尝试：
1. 使用更清晰的音频源
2. 确保音频格式符合要求（16kHz, 16bit, 单声道）
3. 在安静环境中录制音频

### Q: 如何处理大型文档？
A: 建议：
1. 增加系统内存（至少16GB）
2. 调整config.py中的chunk_size参数
3. 分批处理大型文档

### Q: 如何添加对新数据库类型的支持？
A: 需要扩展database_manager.py：
1. 添加新的数据库连接器
2. 实现对应的元数据提取方法
3. 更新数据库选择逻辑

### Q: 如何提高查询响应速度？
A: 优化建议：
1. 使用GPU加速向量计算
2. 优化数据库索引
3. 增加chunk_size减少检索数量
4. 使用缓存机制存储常见查询结果

---

## 🚀 性能优化建议

### 硬件优化
1. 使用GPU加速模型推理和向量计算
2. 增加内存以提高大型文档处理能力
3. 使用SSD存储加快数据库访问速度

### 软件优化
1. 启用向量数据库持久化减少重复计算
2. 实现查询缓存机制
3. 使用异步处理提高并发性能
4. 优化提示词减少LLM响应时间

### 配置优化
1. 调整文本分块参数平衡精度与性能
2. 限制同时处理的文档数量
3. 设置合理的超时和重试机制

---

## 📅 开发计划

### 短期计划
- [ ] 增加对更多音频格式的支持
- [ ] 优化移动端界面体验
- [ ] 添加用户权限管理功能
- [ ] 实现批量文档处理功能

### 中期计划
- [ ] 支持更多数据库类型（MySQL, PostgreSQL）
- [ ] 添加自定义模型部署支持
- [ ] 实现API接口对外提供服务
- [ ] 增加多语言支持

### 长期计划
- [ ] 开发企业级部署方案
- [ ] 实现联邦学习能力
- [ ] 集成更多AI服务（OCR,图像识别）
- [ ] 构建插件生态系统

---

## 🤝 贡献指南

欢迎提交Issue和Pull Request！包括但不限于：

### 代码贡献
1. Fork本仓库
2. 创建特性分支：`git checkout -b feature/AmazingFeature`
3. 提交更改：`git commit -m 'Add some AmazingFeature'`
4. 推送到分支：`git push origin feature/AmazingFeature`
5. 提交Pull Request

### 文档改进
1. 更新README.md中的过时信息
2. 添加使用示例和教程
3. 翻译多语言文档
4. 完善代码注释

### 测试协助
1. 在不同环境中测试系统
2. 提交Bug报告和使用反馈
3. 性能测试和优化建议

### 贡献规范
- 遵循PEP 8代码风格
- 提交前运行现有测试用例
- 更新文档反映代码变化
- 为新增功能添加测试用例

---

## 📄 许可证

本项目采用MIT许可证，详见 [LICENSE](LICENSE) 文件。

### 主要依赖许可证
- Streamlit: Apache 2.0
- LangChain: MIT
- ChromaDB: Apache 2.0
- BGE模型: MIT
- DeepSeek API: 商业许可证

### 使用限制
- 不得用于违法用途
- 需遵守各API服务的条款条件
- 商业使用需注意模型许可证限制

---

## 📮 联系方式

如有问题或合作意向，请联系：

- 📧 Email: 3085237492@qq.com
- 🐙 GitHub: https://github.com/lth-fighting
- 💬 讨论区: https://github.com/lth-fighting/Enterprise-Intelligent-Office-Agent-1.0/discussions
- 🐛 问题报告: https://github.com/lth-fighting/Enterprise-Intelligent-Office-Agent-1.0/issues

### 支持方式
1. 提交GitHub Issue报告Bug
2. 参与Discussions讨论功能建议
3. 提交Pull Request贡献代码
4. 分享使用案例和经验

### 商务合作
对于企业级部署、定制开发或商务合作，请通过邮箱联系。

---

**注意**: 本项目处于积极开发阶段，文档和功能可能随时更新。请定期查看本README获取最新信息。
