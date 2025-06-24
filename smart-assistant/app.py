import streamlit as st
from PyPDF2 import PdfReader
from transformers import pipeline

# Function to read PDF or TXT
def read_file(file):
    if file.name.endswith('.pdf'):
        reader = PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        return text
    else:
        return file.read().decode()

# Load Hugging Face summarizer(force PyTorch)
@st.cache_resource
def load_summarizer():
    return pipeline("summarization", model="google/flan-t5-large", tokenizer="google/flan-t5-large", framework="pt")

summarizer = load_summarizer()

# Streamlit App Title
st.title("📄 Smart Research Assistant")

# File uploader
uploaded_file = st.file_uploader("Upload a PDF or TXT file", type=["pdf", "txt"])

if uploaded_file:
    raw_text = read_file(uploaded_file)
    st.success("✅ Document uploaded!")

    # Summarization
    with st.spinner("Summarizing..."):
        chunks = [raw_text[i:i+3000] for i in range(0, len(raw_text), 3000)]
        summary = ""
        for chunk in chunks:
            result = summarizer(chunk, max_length=150, min_length=50, do_sample=False)
            summary += result[0]["summary_text"] + " "
        st.subheader("📌 Summary (150 words):")
        st.write(summary.strip())

    # Q&A
    st.subheader("💬 Ask Anything")
    user_question = st.text_input("Type your question here:")

    if user_question:
        with st.spinner("Thinking..."):
            prompt = f"Answer the following question based on this text:\n\n{raw_text[:3000]}\n\nQuestion: {user_question}"
            answer_result = summarizer(prompt, max_length=150, min_length=30, do_sample=False)
            st.markdown(f"**Answer:** {answer_result[0]['summary_text']}")

    # Quiz
    st.subheader("🧠 Challenge Me")

    if st.button("Generate Questions"):
        prompt = (
            "Based on the following text, generate 3 logic-based or comprehension-focused questions. "
            "Number them 1 to 3:\n\n" + raw_text[:3000]
        )
        quiz_output = summarizer(prompt, max_length=200, min_length=80, do_sample=False)
        questions = quiz_output[0]['summary_text'].strip().split('\n')

        st.write("### Quiz Questions:")
        for q in questions:
            st.write(q)

        answers = []
        for i in range(1, 4):
            ans = st.text_input(f"Your Answer to Q{i}:")
            answers.append(ans)

        if st.button("Submit Answers"):
            for i, ans in enumerate(answers):
                eval_prompt = (
                    f"Evaluate this answer based on the document.\n"
                    f"Question: {questions[i] if i < len(questions) else 'Q'+str(i+1)}\n"
                    f"Answer: {ans}\n"
                    f"Document: {raw_text[:3000]}\n"
                    f"Give detailed feedback:"
                )
                feedback = summarizer(eval_prompt, max_length=150, min_length=50, do_sample=False)
                st.markdown(f"**Feedback for Q{i+1}:** {feedback[0]['summary_text']}")
