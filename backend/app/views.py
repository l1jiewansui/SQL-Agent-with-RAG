from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from app import app
from app.services.text2sql_service import generate_sql
from app.services.retrieval_service import process_uploaded_file
from app.services.retrieval_service import vector_store, embed_model

UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return "Welcome to SQL Agent API"

@app.route('/test_connection', methods=['GET'])
def test_connection():
    print("Received test connection request")
    return jsonify({'status': 'success', 'message': 'Backend is reachable'})

@app.route('/generate_sql', methods=['POST'])
def generate_sql_route():
    print(f"Request headers: {request.headers}")
    data = request.get_json(force=True)
    print(f"Received data: {data}")
    table_structure = data.get('table_structure')
    user_query = data.get('query')
    file_path = data.get('file_path', None)
    
    if not table_structure or not user_query:
        return jsonify({'error': 'table_structure or user_query missing'}), 400
    
    if file_path:
        # 如果提供了文件路径，处理上传的文件内容
        print(f"Processing file at: {file_path}")
        nodes = process_uploaded_file(file_path)
        context = " ".join([node.text for node in nodes])
    else:
        context = ""
    
    sql_query = generate_sql(table_structure, user_query, context)
    return jsonify({'sql_query': sql_query})

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    
    filename = secure_filename(file.filename)
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(file_path)
    
    # 处理上传的文件并提取文本
    nodes = process_uploaded_file(file_path)
    
    if nodes:
        print(f"添加到向量存储的节点数量: {len(nodes)}")
        vector_store.add(nodes)
    else:
        print("未找到可添加的节点")
        return jsonify({'error': 'No valid text nodes found in the document'}), 400
    
    return jsonify({'message': 'File uploaded successfully', 'nodes': [node.text for node in nodes], 'file_path': file_path})

@app.route('/clear_vector_store', methods=['POST'])
def clear_vector_store():
    try:
        # 清除向量知识库内容
        if vector_store:
            vector_store.clear()
            return jsonify({'status': 'success', 'message': 'Vector store cleared successfully'})
        else:
            return jsonify({'status': 'error', 'message': 'Vector store not initialized'}), 500
    except Exception as e:
        print(f"Error clearing vector store: {str(e)}")
        return jsonify({'status': 'error', 'message': 'Failed to clear vector store', 'error': str(e)}), 500
        
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


#from flask import request, jsonify, render_template
#from app import app
#from app.services.text2sql_service import generate_sql_with_context

#@app.route('/')
#def index():
#    return "Welcome to SQL Agent API"

#@app.route('/test_connection', methods=['GET'])
#def test_connection():
#    print("Received test connection request")
#    return jsonify({'status': 'success', 'message': 'Backend is reachable'})

#@app.route('/generate_sql', methods=['POST'])
#def generate_sql_route():
#    data = request.get_json()
#    table_structure = data.get('table_structure')
#    user_query = data.get('query')
#    sql_query, context = generate_sql_with_context(table_structure, user_query)
#    return jsonify({'sql_query': sql_query, 'context': context})