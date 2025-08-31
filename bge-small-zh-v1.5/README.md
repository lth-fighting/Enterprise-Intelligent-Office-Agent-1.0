# 📁 模型存放与配置指南
本文档详细说明项目所需 **BGE-small-zh-v1.5 嵌入模型** 的下载、放置与验证流程，确保系统正常运行。


## 🎯 目录用途
项目根目录下的 'bge-small-zh-v1.5' 文件夹，用于统一存放自行下载的大语言模型文件，当前主要需放置 **BGE-small-zh-v1.5 嵌入模型**（约100MB+）。  
由于模型文件体积较大，无法直接纳入Git仓库（避免仓库体积超标、下载缓慢），需用户手动下载并按指定结构放置。


## 📥 模型下载与放置步骤
提供两种下载方式，推荐使用 `git-lfs` 确保文件完整性。

### 方法一：使用 git-lfs 下载（推荐）
1. **安装 git-lfs**（若未安装）  
   适用于Windows/macOS/Linux，执行以下命令：
   ```bash
   # 安装 git-lfs（已安装可跳过）
   git lfs install
   ```

2. **克隆模型仓库到指定目录**  
   直接将Hugging Face模型仓库克隆到项目的 `bge-small-zh-v1.5/` 路径：
   ```bash
   git clone https://huggingface.co/BAAI/bge-small-zh-v1.5 ./bge-small-zh-v1.5
   ```


### 方法二：手动下载放置
1. **访问模型页面**  
   打开Hugging Face模型官网：[BAAI/bge-small-zh-v1.5](https://huggingface.co/BAAI/bge-small-zh-v1.5)

2. **下载必需文件**  
   点击页面顶部的 **Files and versions** 选项卡，下载以下核心文件（缺一不可）：
   - `pytorch_model.bin`（模型权重文件）
   - `config.json`（模型配置文件）
   - `tokenizer.json`（分词器词典文件）
   - `tokenizer_config.json`（分词器配置文件）
   - `special_tokens_map.json`（特殊token映射文件）

3. **创建目录结构**  
   在项目根目录手动创建 `models/` 及子目录，最终结构如下：
   ```text
   bge-small-zh-v1.5/
       ├── pytorch_model.bin
       ├── config.json
       ├── tokenizer.json
       ├── tokenizer_config.json
       ├── special_tokens_map.json
       └── README.md  # 可选，模型官方说明
   ```
   将下载的所有文件放入 `./models/bge-small-zh-v1.5/` 目录中。


## ⚙️ 配置文件设置
模型放置完成后，需修改项目配置文件 `config.py`，确保系统能找到模型路径：
```python
# config.py 中修改嵌入模型路径
# 原路径：EMBEDDING_MODEL = "./bge-small-zh-v1.5"
# 新路径（适配 models/ 目录结构）：
EMBEDDING_MODEL = "./bge-small-zh-v1.5"
```


## 🔍 验证模型安装
运行以下命令，快速验证模型是否成功加载（无报错即代表正常）：
```bash
python -c "
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
# 加载本地模型
embeddings = HuggingFaceEmbeddings(model_name='./bge-small-zh-v1.5')
# 生成测试向量（验证功能）
test_vector = embeddings.embed_query('学术文献分析')
print(f'模型加载成功！测试向量维度：{len(test_vector)}')
"
```
- 成功输出：`模型加载成功！测试向量维度：384`（BGE-small-zh-v1.5 输出维度固定为384）
- 若报错：检查文件是否完整、路径是否正确、依赖包是否安装（参考 `requirements.txt`）


## ❓ 常见问题
| 问题 | 解决方案 |
|------|----------|
| Q: 为什么需要手动下载模型？ | A: GitHub对仓库单个文件大小限制为25MB，模型文件（100MB+）超出限制；且手动下载可选择稳定网络环境，避免Git拉取中断。 |
| Q: 下载时缺少部分文件（如 `tokenizer.json`）怎么办？ | A: 刷新Hugging Face模型页面，检查是否有文件更新；或通过 `git-lfs` 重新克隆，确保文件完整性。 |
| Q: 模型加载时报“Out of memory”错误？ | A: 1. CPU环境：确保内存≥8GB，关闭其他占用内存的程序；2. GPU环境：检查CUDA是否配置正确，或改用CPU运行（修改 `documents_processor.py` 中 `device='cpu'`）。 |
| Q: 项目结构是否需要严格遵循？ | A: 是。若自定义模型路径，需同步修改 `config.py` 中的 `EMBEDDING_MODEL` 变量，确保路径与实际存放位置一致。 |


## ⚠️ 注意事项
1. **文件完整性**：缺少任何核心文件（如 `pytorch_model.bin`）会导致模型加载失败，下载后需核对文件列表。
2. **缓存文件**：首次运行系统时，会在 `bge-small-zh-v1.5/` 目录下生成 `.cache/` 文件夹，为PyTorch自动生成的缓存，属于正常现象，无需删除。
3. **内存占用**：CPU运行时，模型加载约占用500MB+内存；GPU运行时（支持CUDA），内存占用会降低，推理速度更快。
4. **模型更新**：若后续需升级模型，直接替换 `./bge-small-zh-v1.5/` 下的文件即可，无需修改其他代码（确保文件名不变）。


## 📞 获取帮助
若遇到模型下载或加载问题，可通过以下途径解决：
1. 查看 **Hugging Face模型官方文档**：[BGE-small-zh-v1.5 Documentation](https://huggingface.co/BAAI/bge-small-zh-v1.5#usage)
2. 查阅项目 **Issues页面**：查看是否有其他用户遇到类似问题及解决方案。
3. 提交新Issue：若问题未解决，可在GitHub/Gitee仓库提交Issue，描述具体错误信息（如报错日志、环境配置），便于协助排查。
