from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# ==========================================
# BAGIAN 1: Inisialisasi Model Embedding
# ==========================================
# Menggunakan BGE-M3 sesuai dengan proposal DietMate AI
print("1. Memuat model embedding BGE-M3...")
embeddings = HuggingFaceEmbeddings(model_name="BAAI/bge-m3")

# ==========================================
# BAGIAN 2: Data Resep & Setup ChromaDB
# ==========================================
print("2. Menyiapkan ChromaDB dan memasukkan resep...")
# Contoh dataset resep sederhana
resep_diet = [
    "Salad Dada Ayam Rebus: 300 kalori, 30g protein. Bahan: Dada ayam 100g, selada, tomat, minyak zaitun. Rebus ayam hingga matang, potong dadu, campur dengan sayuran.",
    "Oatmeal Buah Naga: 250 kalori, 5g protein. Bahan: Oat 50g, susu almond 100ml, buah naga setengah buah. Rebus oat dengan susu, tambahkan potongan buah naga.",
    "Nasi Merah Ikan Panggang: 400 kalori, 35g protein. Bahan: Nasi merah 100g, ikan nila 100g, perasan jeruk nipis. Panggang ikan dengan sedikit garam, sajikan dengan nasi merah.",
    "Telur Orak-Arik Bayam: 200 kalori, 15g protein. Bahan: 2 butir telur, segenggam bayam. Tumis bayam, masukkan telur dan orak-arik hingga matang."
]

# Membuat Vector Store menggunakan ChromaDB
vectorstore = Chroma.from_texts(
    texts=resep_diet, 
    embedding=embeddings,
    collection_name="resep_dietmate"
)

# Membuat retriever untuk mengambil 2 resep paling relevan
retriever = vectorstore.as_retriever(search_kwargs={"k": 2})

# ==========================================
# BAGIAN 3: Inisialisasi LLM Qwen 2.5
# ==========================================
print("3. Menghubungkan ke model LLM Qwen 2.5...")
# Menggunakan Qwen 2.5 via Ollama untuk inferensi lokal yang praktis
llm = ChatOllama(model="qwen2.5", temperature=0.3)

# ==========================================
# BAGIAN 4: Menyusun Prompt RAG
# ==========================================
# Prompt sederhana agar LLM memilih resep dari konteks
template = """
Anda adalah DietMate AI, asisten perencana diet yang ahli.
Berdasarkan resep yang tersedia di bawah ini, buatkan susunan menu makanan sesuai dengan permintaan pengguna.
Jangan menggunakan resep di luar konteks yang diberikan.

Konteks Resep:
{context}

Permintaan Pengguna: {question}

Susunan Menu:
"""
prompt = PromptTemplate.from_template(template)

# ==========================================
# BAGIAN 5: Membangun Chain & Menjalankan Prototipe
# ==========================================
print("4. Menyusun RAG Chain...")
def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# Uji coba prototipe
query = "Tolong buatkan menu makan siang yang tinggi protein untuk membangun massa otot."
print(f"\nPermintaan: {query}\n")
print("Sedang menyusun menu...\n")

hasil = rag_chain.invoke(query)
print("=== HASIL REKOMENDASI DIETMATE AI ===")
print(hasil)