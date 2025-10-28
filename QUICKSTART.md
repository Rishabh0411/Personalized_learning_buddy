# 🚀 QUICK START GUIDE

## Get Started in 5 Minutes!

### Step 1: Navigate to Project Directory
```bash
cd "/home/rishabh/Desktop/Projects/Gen AI Project/personalized_learning_buddy"
```

### Step 2: Run the Quick Start Script
```bash
./start.sh
```

This script will:
- Create a virtual environment
- Install all dependencies
- Create sample test data
- Run setup tests
- Launch the application

### Step 3: Set Up Your API Key

Before the app can generate quizzes, you need an OpenAI API key:

1. Go to https://platform.openai.com/api-keys
2. Create a new API key
3. Edit the `.env` file:
   ```bash
   nano .env
   ```
4. Replace `your_openai_api_key_here` with your actual key
5. Save and exit (Ctrl+X, then Y, then Enter)

### Step 4: Use the Application

The app will open at `http://localhost:8501`

**First-time workflow:**

1. **Upload Notes** (📄 Upload Notes)
   - Click "Browse files" 
   - Upload `data/sample_ml_notes.txt` (created automatically)
   - Click "🚀 Process Documents"
   - Wait for confirmation

2. **Ask Questions** (💬 Chat & Learn)
   - Type: "What is supervised learning?"
   - Click "Ask"
   - Read the AI-generated explanation

3. **Take a Quiz** (📝 Take Quiz)
   - Set topic: "Machine Learning"
   - Adjust number of questions
   - Click "🎯 Generate Quiz"
   - Answer the questions
   - Click "✅ Submit Quiz"
   - See your score!

4. **Track Progress** (📊 Performance)
   - View your accuracy trends
   - See topic-wise performance
   - Review recent quizzes

5. **Get Study Plan** (📅 Study Plan)
   - View personalized recommendations
   - See weak areas that need focus
   - Follow the suggested schedule

---

## Alternative: Manual Setup

If the script doesn't work, follow these steps:

### 1. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Linux/Mac
# OR
venv\Scripts\activate  # On Windows
```

### 2. Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Set Up Environment
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### 4. Create Sample Data
```bash
python create_sample_data.py
```

### 5. Run Tests
```bash
python test_setup.py
```

### 6. Start the App
```bash
streamlit run app.py
```

---

## Troubleshooting

### "Command not found: streamlit"
```bash
pip install streamlit
```

### "No module named 'sentence_transformers'"
```bash
pip install -r requirements.txt
```

### "OpenAI API key not found"
1. Create `.env` file from `.env.example`
2. Add your API key from https://platform.openai.com/api-keys

### "PDF extraction failed"
- Try a different PDF file
- Or use TXT/DOCX format instead

### Port 8501 already in use
```bash
streamlit run app.py --server.port 8502
```

---

## Features Checklist

Test these features after setup:

- [ ] Upload a document (PDF/DOCX/TXT)
- [ ] Process documents successfully
- [ ] Ask a question in chat
- [ ] Get an AI explanation
- [ ] Generate a quiz
- [ ] Take the quiz
- [ ] View performance dashboard
- [ ] See study plan recommendations

---

## Next Steps

1. **Upload Your Own Notes**
   - Lecture notes, textbook chapters, etc.
   - PDF, DOCX, or TXT format
   - Multiple files supported

2. **Customize Settings**
   - Adjust quiz difficulty
   - Change number of questions
   - Focus on specific topics

3. **Track Your Progress**
   - Take quizzes regularly
   - Monitor your improvement
   - Follow the study plan

4. **Share & Collaborate**
   - Share with classmates
   - Study together
   - Compare progress

---

## Getting Help

- **Check README.md** for detailed documentation
- **Read DEVELOPMENT.md** for customization guide
- **Run test_setup.py** to diagnose issues

---

## Tips for Best Results

✅ **DO:**
- Upload clear, well-formatted notes
- Take quizzes regularly (daily/weekly)
- Review incorrect answers
- Follow the personalized study plan
- Upload multiple related documents

❌ **DON'T:**
- Upload scanned images (OCR not supported yet)
- Skip document processing step
- Ignore weak areas identified in study plan
- Submit quizzes without answering all questions

---

## Free API Alternatives

If you don't want to use OpenAI:

1. **Hugging Face (Free)**
   - Sign up at https://huggingface.co/
   - Get free API token
   - Modify `quiz_generator.py` to use Hugging Face models

2. **Local LLM (Free)**
   - Install Ollama: https://ollama.ai/
   - Run models locally
   - No API costs!

---

**Ready to start learning smarter? 🚀**

Run: `./start.sh`
