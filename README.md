# 项目说明文档

## 1. 项目名称

SQL Agent with RAG

## 2. 团队信息

- **团队名称**：t2s
- **队长**：-
- **成员及分工**：
  - **成员1**：-
  - **成员2**：-
- **联系邮箱**：wanghan752@gmail.com

## 3. 项目背景与目的

### 当前市场需求或技术趋势

近年来，人工智能和大数据技术快速发展，特别是在数据分析和自然语言处理领域。企业和组织希望通过自动化工具来优化SQL查询生成，以提高数据查询的效率和准确性。RAG（Retrieval-Augmented Generation）技术结合大语言模型，在大模型强大的SQL生成能力基础上增添了结合业务背景的能力，为实现高质量的自然语言问答提供了新的解决方案。

### 项目动机

随着大数据的普及，许多用户需要从复杂的数据集中提取信息。然而，SQL查询语言的复杂性常常成为用户的障碍。本项目旨在通过简化SQL查询生成过程，帮助用户更轻松地与数据交互。

### 项目希望解决的问题或改进的领域

- **简化SQL查询生成**：自动生成SQL查询语句，减少用户手动编写查询的难度。
- **提高查询的准确性**：利用RAG技术增强生成的准确性和相关性，支持业务知识嵌入。
- **多文件格式支持**：支持PDF、Markdown和文本文件，方便用户上传多种格式的业务文档。

### 项目目标

- **总体目标**：开发一个自动化SQL查询生成系统，支持用户上传业务文档，并生成高质量的SQL查询。
- **具体目标：**
  - 使用本地大语言模型进行自然语言处理。
  - 集成RAG技术，提高生成的准确性。
  - 提供友好的用户界面，支持多种文件格式的上传。

## 4. 方案介绍

### 核心思想和原理

本项目结合了RAG技术和大语言模型，通过检索相关领域知识并结合用户的自然语言查询，生成精确的SQL查询语句。

### 主要功能和特点

- **自然语言问答**：支持用户输入自然语言问题并自动生成对应的SQL查询语句。
- **RAG增强**：利用向量数据库检索相关参考内容，提高生成的准确性。
- **多文件格式支持**：支持PDF、Markdown和文本文件的上传和处理。

### 设计思路和实施步骤

- **数据收集与处理**：
  - 从上传的文件中提取结构化信息。
  - 利用大语言模型对数据进行处理和分析。
- **问答系统开发**：
  - 使用本地大语言模型进行生成。
  - 实现用户查询的解析和处理。
- **用户界面开发**：
  - 采用Gradio框架，提供友好的Web界面。
- **系统优化与部署**：
  - 使用本地大语言模型和向量数据库优化系统性能和响应速度。

## 5. 技术特点

### 使用的算法、模型及数据集

- **大语言模型**：目前使用GLM-4-9B-Chat，用于自然语言理解和生成。同时在text2sql_service.py有支持通义千问闭源模型api的方案，用于测试。ipex-llm（Intel® Extension for PyTorch Large Language Models）用于在 CPU 上优化和加速大语言模型的推理过程，确保在魔搭社区的 CPU 环境中高效运行。
- **向量数据库**：Chroma，用于存储和检索参考文档。

### 数据处理和分析的方法

- **文件处理**：支持PDF、Markdown和文本文件，提取其中的内容并存储为向量。

### 系统架构和模块设计

系统采用模块化设计，包括文件处理、向量检索、模型生成和用户界面模块。

## 6. 使用到的英特尔软硬件技术

项目硬件使用魔搭社区提供的免费云CPU资源 Intel(R) Xeon(R) Platinum 8369B CPU @ 2.70GHz，核心数8；（测试在本地，CPU为*i5*-13600KF）

部署工具采用英特尔 IPEX-LLM ，加速常用大语言模型在英特尔CPU 上的高速推理。

## 7. 成果说明

### 已实现的功能和项目展示的实际效果

- 支持多种文件格式的上传和处理。
- 自动生成高质量的SQL查询语句。
- 提供用户友好的Web界面，支持自然语言查询。

### 性能指标、提升等对比信息

![output](https://pic.imgdb.cn/item/66b08847d9c307b7e93f8b47.png)

![image-20240805120750515](https://pic.imgdb.cn/item/66b08837d9c307b7e93f7c5a.png)

### 运行结果记录或截图

![image-20240805120651474](https://pic.imgdb.cn/item/66b087fed9c307b7e93f4a02.png)


![image-20240805120714817](https://pic.imgdb.cn/item/66b0881bd9c307b7e93f61ce.png)

### 对未来应用和推广的展望

未来可以进一步优化模型性能，支持更多数据库和复杂查询场景。并且在生成sql的基础上，直接在数据库上运行并可视化结果。

## 9. 程序运行指引

### 前端运行

1. **安装依赖**：运行以下命令安装依赖：

   ```
   pip install -r requirements.txt
   ```

2. **启动Gradio界面**： 在 `gradio_ui` 目录下，运行以下命令启动前端界面：

   ```
   python gradio_ui/ui.py
   ```

   这将启动一个Web界面，用户可以通过上传文件和输入查询来生成SQL。

### 后端运行

1. **安装依赖**： 运行以下命令安装依赖：

   ```
   pip install -r requirements.txt
   ```

2. **启动Flask服务**： 在 `backend` 目录下，运行以下命令启动Flask后端服务：

   ```
   python backend/run.py
   ```

3. **上传文档**：

   - 通过前端界面上传PDF、Markdown或文本文件。
   - 文件上传后，系统会自动处理并存储文件中的结构化信息。

4. **生成SQL查询**：

   - 在前端界面输入表结构和自然语言查询，系统将生成对应的SQL查询语句。

## 10. 支持材料（可选）

- **Github链接**：[l1jiewansui/SQL-Agent-with-RAG: This project combines RAG technology and large language models to generate accurate SQL queries by retrieving relevant domain knowledge and incorporating the user's natural language queries. (github.com)](https://github.com/l1jiewansui/SQL-Agent-with-RAG)
- **PPT附件**：附件中
- **演示视频**：附件中
