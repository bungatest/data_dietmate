
# DietMate AI - RAG Module

Modul Retrieval-Augmented Generation (RAG) DietMate AI.

## Teknologi
- Embedding: BAAI/bge-m3
- Vector Database: ChromaDB
- Framework: LangChain
- LLM: Qwen 2.5
- LLM Runtime: Ollama

## Persyaratan
- Python 3.10 atau lebih baru
- Ollama sudah terinstal
- Model Qwen 2.5 tersedia di Ollama

## Instalasi

Buat virtual environment:

```bash
python -m venv .venv
```

Aktifkan virtual environment di Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install dependency:

```bash
pip install -r requirements.txt
```

Unduh model Qwen:

```bash
ollama pull qwen2.5
```

## Menjalankan prototipe

```bash
python RAG.py
```

Pada penggunaan pertama, model embedding BGE-M3 akan diunduh secara otomatis jika belum tersedia secara lokal.

## Catatan pengembangan

Versi saat ini masih berupa prototipe awal:
- Data resep masih menggunakan empat contoh resep hardcode.
- Retrieval mengambil dua resep paling relevan.
- ChromaDB belum menggunakan persistent storage.
- Belum terhubung dengan dataset utama DietMate.
- Belum tersedia API FastAPI.
- Output LLM masih berupa teks.

Pengembangan berikutnya mencakup integrasi dataset resep, persistent vector database, retrieval berdasarkan profil pengguna, dan integrasi backend FastAPI.
