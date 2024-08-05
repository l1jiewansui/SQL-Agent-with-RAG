from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.schema import TextNode, NodeWithScore
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.vector_stores import VectorStoreQuery
import os
import chromadb
from llama_index.readers.file import PyMuPDFReader
import markdown
import codecs

class Config:
    api_key = "YOUR_TONGYIQIANWEN_API_KEY"
    persist_dir = "./chroma_db"
    embedding_model_path = "/data/models/text2vec-large-chinese"

config = Config()
embed_model = HuggingFaceEmbedding(model_name=config.embedding_model_path)

def load_vector_database(persist_dir: str) -> ChromaVectorStore:
    if os.path.exists(persist_dir):
        print(f"加载已有的向量数据库: {persist_dir}")
        chroma_client = chromadb.PersistentClient(path=persist_dir)
        chroma_collection = chroma_client.get_collection("llama2_paper")
    else:
        print(f"创建新的向量数据库: {persist_dir}")
        chroma_client = chromadb.PersistentClient(path=persist_dir)
        chroma_collection = chroma_client.create_collection("llama2_paper")
    print(f"向量存储已加载，包含 {chroma_collection.count()} 个文档")
    return ChromaVectorStore(chroma_collection=chroma_collection)
    
vector_store = load_vector_database(persist_dir=config.persist_dir)

def process_uploaded_file(file_path: str) -> list[TextNode]:
    file_extension = os.path.splitext(file_path)[1].lower()
    text_chunks = []

    if file_extension == ".pdf":
        text_chunks = process_pdf(file_path)
    elif file_extension == ".md":
        text_chunks = process_markdown(file_path)
    elif file_extension == ".txt":
        text_chunks = process_txt(file_path)
    else:
        print(f"不支持的文件格式: {file_extension}")
    
    if not text_chunks:
        print("未提取到任何文本内容")
    else:
        print(f"提取到的文本块数量: {len(text_chunks)}")
    
    # 为每个文本块生成嵌入
    nodes = []
    for chunk in text_chunks:
        embedding = embed_model.get_text_embedding(chunk.text) # 计算嵌入
        node = TextNode(text=chunk.text, embedding=embedding)
        nodes.append(node)
    
    return nodes

def process_pdf(file_path: str) -> list[TextNode]:
    loader = PyMuPDFReader()
    documents = loader.load(file_path=file_path)

    text_parser = SentenceSplitter(chunk_size=50)
    text_chunks = []
    for doc in documents:
        cur_text_chunks = text_parser.split_text(doc.text)
        for chunk in cur_text_chunks:
            text_chunks.append(TextNode(text=chunk, metadata=doc.metadata))
    return text_chunks

def process_markdown(file_path: str) -> list[TextNode]:
    with codecs.open(file_path, mode="r", encoding="utf-8") as f:
        md_content = f.read()
    html_content = markdown.markdown(md_content)
    text_parser = SentenceSplitter(chunk_size=384)
    text_chunks = text_parser.split_text(html_content)
    return [TextNode(text=chunk) for chunk in text_chunks]

def process_txt(file_path: str) -> list[TextNode]:
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    text_parser = SentenceSplitter(chunk_size=384)
    text_chunks = text_parser.split_text(content)
    return [TextNode(text=chunk) for chunk in text_chunks]

class VectorDBRetriever:
    def __init__(self, vector_store: ChromaVectorStore, embed_model: HuggingFaceEmbedding, query_mode: str = "default", similarity_top_k: int = 2):
        self._vector_store = vector_store
        self._embed_model = embed_model
        self._query_mode = query_mode
        self._similarity_top_k = similarity_top_k

    def retrieve(self, query_embedding: list[float]) -> list[NodeWithScore]:
        vector_store_query = VectorStoreQuery(query_embedding=query_embedding, similarity_top_k=self._similarity_top_k, mode=self._query_mode)
        query_result = self._vector_store.query(vector_store_query)

        nodes_with_scores = []
        for index, node in enumerate(query_result.nodes):
            score: Optional[float] = None
            if query_result.similarities is not None:
                score = query_result.similarities[index]
            nodes_with_scores.append(NodeWithScore(node=node, score=score))
        print(f"检索到 {len(nodes_with_scores)} 个节点")
        return nodes_with_scores

    def clear(self):
        # 清除向量存储中的所有内容
        self._vector_store.chroma_collection.clear()
        print("Vector store cleared")
        
retriever = VectorDBRetriever(vector_store, embed_model)

def retrieve(query_embedding):
    nodes_with_scores = retriever.retrieve(query_embedding)
    return [node_with_score.node.text for node_with_score in nodes_with_scores]
