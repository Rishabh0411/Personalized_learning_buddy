# Personalized Learning Buddy - Development Guide

## 📋 Component Details

### 1. RAG Pipeline (rag_pipeline.py)

**Responsibilities:**
- Document text extraction (PDF, DOCX, TXT)
- Text chunking using RecursiveCharacterTextSplitter
- Embedding generation using SentenceTransformers
- FAISS index management
- Retrieval of relevant chunks

**Key Methods:**
- `process_document()`: Extract and chunk text from files
- `create_embeddings()`: Generate embeddings for chunks
- `build_index()`: Create/update FAISS index
- `retrieve()`: Find top-k relevant chunks for a query
- `save_vectorstore()`: Persist index to disk
- `load_vectorstore()`: Load index from disk

**Testing:**
```python
from rag_pipeline import RAGPipeline

rag = RAGPipeline()
docs = rag.process_document("data/sample_ml_notes.txt")
rag.build_index(docs)
results = rag.retrieve("What is supervised learning?")
```

### 2. Quiz Generator (quiz_generator.py)

**Responsibilities:**
- Generate MCQs using OpenAI API
- Generate True/False questions
- Generate Short Answer questions
- Explain difficult concepts

**Key Methods:**
- `generate_mcqs()`: Create multiple choice questions
- `generate_true_false()`: Create T/F questions
- `generate_short_answer()`: Create short answer questions
- `generate_mixed_quiz()`: Combine all question types
- `explain_concept()`: Generate explanations

**Testing:**
```python
from quiz_generator import QuizGenerator

quiz_gen = QuizGenerator()
context = "Machine learning is a subset of AI..."
mcqs = quiz_gen.generate_mcqs(context, num_questions=3)
```

### 3. Evaluator (evaluate.py)

**Responsibilities:**
- Record quiz attempts
- Calculate performance metrics
- Track progress over time
- Generate study plans
- Identify weak areas

**Key Methods:**
- `record_quiz_attempt()`: Save quiz results
- `get_overall_statistics()`: Overall performance metrics
- `get_topic_performance()`: Topic-wise breakdown
- `get_weak_areas()`: Identify struggling topics
- `generate_study_plan()`: Create personalized plan

**Testing:**
```python
from evaluate import QuizEvaluator

evaluator = QuizEvaluator()
# Record a quiz attempt
result = evaluator.record_quiz_attempt(
    quiz_id="test_1",
    questions=questions,
    answers=user_answers,
    topic="ML Basics"
)
```

### 4. Streamlit App (app.py)

**Responsibilities:**
- User interface
- File upload handling
- Chat interface
- Quiz presentation
- Performance visualization

**Pages:**
1. Upload Notes
2. Chat & Learn
3. Take Quiz
4. Performance Dashboard
5. Study Plan

## 🔧 Customization Guide

### Adding New Question Types

Edit `quiz_generator.py`:

```python
def generate_fill_in_blank(self, context: str, num_questions: int = 5):
    """Generate fill-in-the-blank questions"""
    prompt = f"""Generate {num_questions} fill-in-the-blank questions..."""
    # Implementation
```

### Using Different Embedding Models

Edit `rag_pipeline.py`:

```python
# Change the model in __init__
def __init__(self, embedding_model_name: str = "all-mpnet-base-v2"):
    # Larger model = better quality but slower
```

Popular alternatives:
- `all-MiniLM-L6-v2` (default, fast, 384 dim)
- `all-mpnet-base-v2` (better quality, 768 dim)
- `paraphrase-multilingual-MiniLM-L12-v2` (multilingual)

### Using Different Vector Stores

Replace FAISS with ChromaDB in `rag_pipeline.py`:

```python
import chromadb

class RAGPipeline:
    def __init__(self):
        self.client = chromadb.Client()
        self.collection = self.client.create_collection("documents")
```

### Adding Authentication

Add to `app.py`:

```python
import streamlit_authenticator as stauth

# Add before main()
authenticator = stauth.Authenticate(
    credentials,
    'cookie_name',
    'signature_key',
    cookie_expiry_days=30
)

name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    main()
```

## 🎯 Common Tasks

### Task 1: Add New Document Type (e.g., Markdown)

Edit `rag_pipeline.py`:

```python
def extract_text_from_md(self, md_path: str) -> str:
    """Extract text from Markdown file"""
    import markdown
    with open(md_path, 'r', encoding='utf-8') as file:
        md_content = file.read()
        html = markdown.markdown(md_content)
        # Convert HTML to text
        return html

# Update process_document()
elif file_extension == '.md':
    text = self.extract_text_from_md(file_path)
```

### Task 2: Add Difficulty Levels to Quizzes

Edit `quiz_generator.py`:

```python
def generate_mcqs(self, context: str, num_questions: int = 5, difficulty: str = "medium"):
    prompt = f"""Generate {num_questions} {difficulty} difficulty MCQs..."""
```

### Task 3: Export Quiz Results to PDF

Add to `evaluate.py`:

```python
from reportlab.pdfgen import canvas

def export_to_pdf(self, filename: str):
    """Export quiz results to PDF"""
    c = canvas.Canvas(filename)
    # Add content
    c.save()
```

### Task 4: Add Email Reminders

```python
import smtplib
from email.mime.text import MIMEText

def send_reminder(email: str):
    msg = MIMEText("Time to study!")
    msg['Subject'] = 'Study Reminder'
    msg['From'] = 'your_email@gmail.com'
    msg['To'] = email
    
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login('your_email', 'password')
        server.send_message(msg)
```

## 🐛 Debugging Tips

### Issue: Embeddings are slow
**Solution:** Reduce chunk size or use batch processing

```python
# In rag_pipeline.py
embeddings = self.embedding_model.encode(
    texts, 
    batch_size=32,  # Process in batches
    show_progress_bar=True
)
```

### Issue: Quiz generation fails
**Solution:** Check API key and implement retry logic

```python
import time
from openai import OpenAI

def generate_with_retry(self, prompt, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = self.client.chat.completions.create(...)
            return response
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
            else:
                raise e
```

### Issue: Memory problems with large documents
**Solution:** Process documents in smaller batches

```python
def process_large_document(self, file_path: str, batch_size: int = 100):
    all_docs = self.process_document(file_path)
    
    for i in range(0, len(all_docs), batch_size):
        batch = all_docs[i:i + batch_size]
        self.build_index(batch)
```

## 📊 Performance Optimization

### 1. Cache Embeddings
```python
import functools

@functools.lru_cache(maxsize=1000)
def get_embedding(text: str):
    return model.encode(text)
```

### 2. Use GPU for Embeddings
```python
model = SentenceTransformer('all-MiniLM-L6-v2', device='cuda')
```

### 3. Optimize FAISS Index
```python
# Use IVF index for large datasets
quantizer = faiss.IndexFlatL2(dimension)
index = faiss.IndexIVFFlat(quantizer, dimension, nlist=100)
```

## 🚀 Deployment

### Deploy on Streamlit Cloud

1. Push code to GitHub
2. Go to https://streamlit.io/cloud
3. Connect repository
4. Add secrets (OpenAI API key)
5. Deploy!

### Deploy on Heroku

```bash
# Create Procfile
echo "web: streamlit run app.py --server.port=$PORT" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

## 📚 Additional Resources

- [LangChain Documentation](https://python.langchain.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [FAISS Documentation](https://faiss.ai/)
- [OpenAI API Reference](https://platform.openai.com/docs/)

## 🤝 Contributing Workflow

1. Fork the repository
2. Create a feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## 📝 Code Style

Follow PEP 8 guidelines:
```bash
pip install black flake8
black .
flake8 .
```
