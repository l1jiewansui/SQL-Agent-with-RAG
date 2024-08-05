# import openai

# # 设置API密钥
# openai.api_key = '*'

# def generate_sql(table_structure, query):
#     # 调用OpenAI API进行自然语言处理
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[
#             {"role": "system", "content": "You are a SQL generation assistant. Generate SQL queries based on the given table structure and user query."},
#             {"role": "user", "content": f"Table structure: {table_structure}\nUser query: {query}\nGenerate the corresponding SQL query."}
#         ],
#         max_tokens=150
#     )
#     sql_query = response.choices[0].message['content'].strip()
#     return sql_query

#通义千问

# import dashscope
# from .retrieval_service import retrieve, embed_model

# # 如果环境变量配置无效请启用以下代码
# dashscope.api_key = '*'

# def generate_sql(table_structure, query, context=""):
#     # 获取查询的嵌入向量
#     query_embedding = embed_model.get_query_embedding(query)
#     # 使用RAG技术检索相关文本
#     retrieved_texts = retrieve(query_embedding)
#     context = " ".join(retrieved_texts)
#     print(f"RAG参考内容: {context}")
    
#     # 定义消息列表，包含系统提示和用户输入
#     messages = [
#         {'role': 'system', 'content': '你是一个SQL生成助手。根据提供的表结构和用户查询生成SQL查询语句，并且只返回一段完整的SQL语句。请注意，参考内容仅供参考。'},
#         {'role': 'user', 'content': f'表结构: {table_structure}\n用户查询: {query}\n参考内容: {context}\n生成对应的SQL查询语句。'}
#     ]
    
#     # 调用通义千问API生成SQL查询
#     response = dashscope.Generation.call(
#         dashscope.Generation.Models.qwen_turbo,
#         messages=messages,
#         result_format='message',
#         #max_tokens=200  # 设置token上限为1500（或根据需求调整）
#     )
#     # 获取生成的SQL查询语句
#     sql_query = response['output']['choices'][0]['message']['content'].strip()
#     return sql_query

from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from .retrieval_service import retrieve, embed_model

# 加载本地的大模型和分词器
model_name = "/data/models/glm-4-9b-chat"  # 这里替换为本地模型的路径
model = AutoModelForCausalLM.from_pretrained(model_name, trust_remote_code=True)
tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)

def generate_sql(table_structure, query, context=""):
    query_embedding = embed_model.get_query_embedding(query)
    retrieved_texts = retrieve(query_embedding)
    context = " ".join(retrieved_texts)
    print(f"RAG参考内容: {context}")
    
    prompt = (
        "你是一个SQL生成助手。根据提供的表结构和用户查询生成SQL查询语句，并且只返回一段完整的SQL语句。"
        "请注意，参考内容仅供参考。\n"
        f"表结构: {table_structure}\n用户查询: {query}\n参考内容: {context}\n生成对应的SQL查询语句。"
    )
    
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=400)
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True).strip()
    
    # 提取SQL部分，仅保留 ```sql 和 ``````sql 之间的内容
    if "```sql" in generated_text and "``````sql" in generated_text:
        start = generated_text.find("```sql") + len("```sql")
        end = generated_text.find("``````sql", start)
        sql_query = generated_text[start:end].strip()
    elif "```sql" in generated_text and "```" in generated_text:
        start = generated_text.find("```sql") + len("```sql")
        end = generated_text.find("```", start)
        sql_query = generated_text[start:end].strip()
    else:
        sql_query = generated_text
    
    return sql_query
