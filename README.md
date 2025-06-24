# 📄 Smart Research Assistant

An AI-powered tool that helps users upload PDF or TXT files, get concise summaries, ask context-aware questions, and receive logical comprehension challenges — all in one place.

---

## 🚀 Features

- 📑 Upload PDF or TXT documents
- ✨ Summarize lengthy documents in under 150 words
- 💬 Ask questions based on the document content
- 🧠 Generate logic/comprehension-based questions from the file
- ✅ Get real-time feedback on your answers

---

## 🛠️ Tech Stack

- **Frontend**: Streamlit  
- **Backend/AI**:  
  - OpenAI API (`gpt-3.5-turbo`) or local model (`flan-t5-large`)  
  - LangChain for LLM chain logic  
  - HuggingFace Transformers  
- **Libraries**:  
  - PyPDF2  
  - Transformers  
  - Streamlit  
  - LangChain  
  - OpenAI  

---

## ⚙️ Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/smart-research-assistant.git
cd smart-research-assistant


# Run the App
streamlit run app.py

