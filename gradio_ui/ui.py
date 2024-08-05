import gradio as gr
import requests

def generate_sql(table_structure, query):
    try:
        response = requests.post(
            "http://127.0.0.1:5000/generate_sql", 
            json={"table_structure": table_structure, "query": query}, 
            headers={"Content-Type": "application/json; charset=utf-8"}
        )
        response.raise_for_status()
        return response.json().get('sql_query')
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"

def upload_file(file):
    try:
        with open(file.name, 'rb') as f:
            response = requests.post("http://127.0.0.1:5000/upload", files={"file": f})
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def generate_sql_with_uploaded_file(table_structure, query, file):
    if file is not None:
        upload_response = upload_file(file)
        if 'error' in upload_response:
            return upload_response['error']
        nodes_text = " ".join(upload_response.get('nodes', []))
        query = f"{nodes_text}\n{query}"
    
    return generate_sql(table_structure, query)

def clear_vector_store():
    try:
        response = requests.post("http://127.0.0.1:5000/clear_vector_store")
        response.raise_for_status()
        return response.json().get('message')
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"

# 定义 Gradio 界面
with gr.Blocks() as demo:
    # 插入自定义 CSS
    gr.HTML("""
    <style>
    body, html {
        background-color: #f0f0f0;
        color: #333;
        height: 100%;
        margin: 0;
        font-family: Arial, sans-serif;
    }
    .gradio-container {
        background-color: #fff;
        color: #333;
        border: 1px solid #ccc;
        border-radius: 8px;
        padding: 20px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .gr-input, .gr-textbox, .gr-button {
        background-color: #fff;
        color: #333;
        border: 1px solid #ccc;
        border-radius: 4px;
    }
    .gr-button {
        background-color: #007BFF;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 8px 16px;
        cursor: pointer;
    }
    .gr-button:hover {
        background-color: #0056b3;
    }
    </style>
    """)

    # 添加标题背景图
    gr.HTML("""
    <div style="background-image: url('https://pic.imgdb.cn/item/66b03f37d9c307b7e9e1ac18.png'); background-size: cover; padding: 20px; text-align: center; border-radius: 8px;">
        <h1 style="color: #333; font-size: 2rem;">SQL Agent with RAG</h1>
        <p style="color: #555;">智能SQL生成助手</p>
    </div>
    """)

    with gr.Row(elem_id="input-section"):
        with gr.Column(scale=3):
            table_structure = gr.Textbox(lines=10, label="表结构", placeholder="在此输入表结构...")
            query = gr.Textbox(lines=2, label="查询", placeholder="在此输入您的SQL查询请求...")
            file_upload = gr.File(label="上传您的文档")

        with gr.Column(scale=1):
            generate_btn = gr.Button("生成 SQL")
            clear_btn = gr.Button("清空向量存储")
            output = gr.Textbox(label="生成的 SQL", placeholder="生成的 SQL 查询将显示在这里...")

    gr.Markdown(
        """
        ### 使用说明
        1. 在提供的文本框中输入表结构，例如CREATE TABLE...
        2. 在查询框中描述您的查询。
        3. 可选择上传一个文档以执行RAG。
        4. 点击“生成 SQL”以创建 SQL 查询。
        5. 点击“清空向量存储”以重置文档存储。
        """,
        elem_id="instructions"
    )

    # 定义按钮的动作
    generate_btn.click(
        generate_sql_with_uploaded_file, 
        inputs=[table_structure, query, file_upload], 
        outputs=output
    )

    clear_btn.click(
        clear_vector_store,
        inputs=[],
        outputs=output
    )

demo.launch(share=True)
