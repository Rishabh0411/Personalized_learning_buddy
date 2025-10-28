# 🔧 Troubleshooting Guide

## Common Issues and Solutions

---

## 1. Installation Issues

### Issue: `pip install` fails

**Symptoms:**
```
ERROR: Could not find a version that satisfies the requirement...
```

**Solutions:**
```bash
# Update pip first
pip install --upgrade pip

# Try installing with --no-cache-dir
pip install --no-cache-dir -r requirements.txt

# Install packages one by one
pip install streamlit
pip install langchain
# etc.
```

### Issue: Python version too old

**Symptoms:**
```
Python 3.6 is not supported
```

**Solution:**
```bash
# Check your Python version
python3 --version

# Install Python 3.8 or higher
# On Ubuntu/Debian:
sudo apt update
sudo apt install python3.10

# Create venv with specific version
python3.10 -m venv venv
```

---

## 2. API Key Issues

### Issue: "OpenAI API key not found"

**Symptoms:**
- Quiz generation doesn't work
- Error message about missing API key

**Solutions:**

1. **Create .env file:**
```bash
cp .env.example .env
```

2. **Edit .env file:**
```bash
nano .env
# Add your key:
# OPENAI_API_KEY=sk-your-actual-key-here
```

3. **Verify .env is loaded:**
```python
# Test in Python
from dotenv import load_dotenv
import os
load_dotenv()
print(os.getenv("OPENAI_API_KEY"))
```

### Issue: "Invalid API key"

**Symptoms:**
```
openai.error.AuthenticationError: Incorrect API key
```

**Solutions:**
- Get a new key from https://platform.openai.com/api-keys
- Check for extra spaces in .env file
- Make sure key starts with "sk-"
- Verify you have credits: https://platform.openai.com/account/usage

---

## 3. Document Processing Issues

### Issue: PDF text extraction fails

**Symptoms:**
- Empty text extracted
- "No text could be extracted" error

**Solutions:**

1. **Try different PDF:**
```python
# Some PDFs are scanned images
# Use OCR tools like pytesseract for image-based PDFs
```

2. **Check PDF quality:**
- Re-save PDF from another reader
- Convert scanned PDF to text PDF
- Use TXT or DOCX format instead

3. **Manual text extraction:**
```bash
# Use pdftotext command
pdftotext yourfile.pdf output.txt
# Then upload output.txt
```

### Issue: DOCX extraction fails

**Symptoms:**
```
Error extracting DOCX
```

**Solutions:**
- Open in Microsoft Word/LibreOffice and save again
- Convert to PDF or TXT
- Check if file is corrupted

---

## 4. Embedding & RAG Issues

### Issue: "FAISS index is empty"

**Symptoms:**
- No results when asking questions
- Empty retrieval

**Solutions:**
1. **Upload and process documents first**
2. **Check if vectorstore was saved:**
```bash
ls -lh embeddings/
# Should see vectorstore.pkl
```

3. **Rebuild index:**
- Delete `embeddings/vectorstore.pkl`
- Re-upload documents

### Issue: Slow embedding generation

**Symptoms:**
- Processing takes forever

**Solutions:**
```python
# In rag_pipeline.py, adjust chunk size
self.text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,  # Increase this
    chunk_overlap=100,
)

# Or use GPU
model = SentenceTransformer('all-MiniLM-L6-v2', device='cuda')
```

---

## 5. Quiz Generation Issues

### Issue: Quiz generation fails

**Symptoms:**
```
Error generating MCQs
```

**Solutions:**

1. **Check API rate limits:**
```python
# Add delay between requests
import time
time.sleep(1)
```

2. **Reduce number of questions:**
- Start with 2-3 questions
- Gradually increase

3. **Check context length:**
```python
# Make sure context isn't too long
context = context[:4000]  # Limit to 4000 chars
```

### Issue: Low quality questions

**Symptoms:**
- Questions don't make sense
- Incorrect answers marked as correct

**Solutions:**
- Use more specific topics
- Upload better quality notes
- Increase chunk overlap in RAG
- Adjust temperature in quiz generator:
```python
temperature=0.5  # Lower = more focused
```

---

## 6. Streamlit Issues

### Issue: Port 8501 already in use

**Symptoms:**
```
OSError: [Errno 98] Address already in use
```

**Solutions:**
```bash
# Use different port
streamlit run app.py --server.port 8502

# Or kill existing process
lsof -i :8501
kill -9 <PID>
```

### Issue: Streamlit not found

**Symptoms:**
```
streamlit: command not found
```

**Solutions:**
```bash
# Make sure venv is activated
source venv/bin/activate

# Install streamlit
pip install streamlit

# Run with full path
python -m streamlit run app.py
```

### Issue: Page doesn't refresh

**Symptoms:**
- Changes not showing
- Stuck loading

**Solutions:**
- Press `R` to rerun
- Clear browser cache (Ctrl + Shift + R)
- Restart Streamlit server
- Check browser console for errors

---

## 7. Performance Issues

### Issue: App is slow

**Solutions:**

1. **Cache embeddings:**
```python
@st.cache_resource
def load_rag_pipeline():
    return RAGPipeline()
```

2. **Reduce chunk size:**
```python
chunk_size=300  # Smaller chunks
```

3. **Limit document size:**
```python
# Only process first 50 pages
max_pages = 50
```

4. **Use GPU if available:**
```python
device = 'cuda' if torch.cuda.is_available() else 'cpu'
model = SentenceTransformer('all-MiniLM-L6-v2', device=device)
```

### Issue: High memory usage

**Solutions:**
```bash
# Monitor memory
top -p $(pgrep -f streamlit)

# Clear cache
rm -rf embeddings/vectorstore.pkl
# Re-process documents
```

---

## 8. Data Persistence Issues

### Issue: Quiz results not saving

**Symptoms:**
- Results disappear after refresh
- quiz_results.json not created

**Solutions:**
```bash
# Check permissions
ls -l data/
chmod 755 data/

# Verify file creation
python -c "from evaluate import QuizEvaluator; e = QuizEvaluator(); print(e.results_file)"
```

### Issue: Vectorstore not loading

**Symptoms:**
- Have to re-process documents every time

**Solutions:**
```bash
# Check if file exists
ls -lh embeddings/vectorstore.pkl

# Verify it's not corrupted
python -c "import pickle; pickle.load(open('embeddings/vectorstore.pkl', 'rb'))"

# Rebuild if corrupted
rm embeddings/vectorstore.pkl
# Re-upload documents
```

---

## 9. Testing Issues

### Issue: test_setup.py fails

**Solutions:**
```bash
# Run with verbose output
python -v test_setup.py

# Test components individually
python -c "from rag_pipeline import RAGPipeline; print('OK')"
python -c "from quiz_generator import QuizGenerator; print('OK')"
python -c "from evaluate import QuizEvaluator; print('OK')"
```

---

## 10. Deployment Issues

### Issue: Streamlit Cloud deployment fails

**Solutions:**

1. **Add requirements.txt** to root
2. **Create packages.txt** for system dependencies:
```
libpoppler-cpp-dev
```

3. **Add secrets** in Streamlit Cloud dashboard:
```toml
OPENAI_API_KEY = "sk-your-key"
```

4. **Check Python version** in Streamlit Cloud settings

---

## 🆘 Emergency Fixes

### Nuclear Option: Fresh Start

```bash
# Backup your data
cp -r data/ data_backup/

# Remove everything
rm -rf venv/
rm -rf embeddings/
rm -rf __pycache__/
rm data/quiz_results.json

# Start fresh
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python create_sample_data.py
streamlit run app.py
```

---

## 📞 Getting More Help

### Debug Mode

```bash
# Run with debug logging
streamlit run app.py --logger.level=debug
```

### Check Logs

```bash
# Streamlit logs
cat ~/.streamlit/logs/streamlit.log

# Python errors
python app.py 2>&1 | tee error.log
```

### Report Issues

When asking for help, include:
1. Error message (full traceback)
2. Python version: `python3 --version`
3. OS: `uname -a`
4. What you were doing when error occurred
5. Steps to reproduce

---

## 🔍 Diagnostic Commands

```bash
# Check Python
python3 --version

# Check pip
pip --version

# List installed packages
pip list

# Check API key
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('OK' if os.getenv('OPENAI_API_KEY') else 'NOT FOUND')"

# Test OpenAI
python -c "import openai; print('OpenAI version:', openai.__version__)"

# Check Streamlit
streamlit --version

# Test FAISS
python -c "import faiss; print('FAISS OK')"

# Test SentenceTransformers
python -c "from sentence_transformers import SentenceTransformer; print('ST OK')"
```

---

## 💡 Prevention Tips

1. **Always activate venv** before working
2. **Keep .env file secure** (don't commit to git)
3. **Regular backups** of data/ folder
4. **Update dependencies** periodically:
   ```bash
   pip install --upgrade -r requirements.txt
   ```
5. **Test after changes** with test_setup.py
6. **Monitor API usage** to avoid unexpected bills
7. **Use git** for version control

---

## ✅ Quick Health Check

Run this to verify everything is working:

```bash
python test_setup.py
```

Should show all ✅ if everything is OK!

---

**Still having issues? Check the FAQ in README.md or create an issue on GitHub!**
