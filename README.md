# 🧠 Personalized Learning Buddy

Transform your study experience with AI! Upload your notes and get personalized quizzes, concept explanations, and smart study plans.

## 🚀 Features

- **📄 Document Processing**: Upload PDF, DOCX, or TXT files
- **🔍 RAG Pipeline**: Intelligent retrieval of relevant content from your notes
- **💬 Interactive Chat**: Ask questions and get clear explanations
- **📝 Quiz Generation**: Auto-generated MCQs, True/False, and Short Answer questions
- **📊 Performance Tracking**: Visualize your progress over time
- **📅 Smart Study Plans**: Personalized recommendations based on your performance

## 🛠️ Tech Stack

- **Backend**: Python
- **LLM**: OpenAI GPT-3.5-turbo
- **Retrieval**: TF-IDF + cosine similarity
- **Frontend**: Streamlit
- **Visualization**: Plotly

## 📁 Project Structure

```
personalized_learning_buddy/
│
├── data/                  # Uploaded notes (auto-created)
├── embeddings/            # Vector DB files (auto-created)
├── rag_pipeline.py        # RAG logic - Document processing & retrieval
├── quiz_generator.py      # Quiz generation using LLM
├── evaluate.py            # Performance tracking & metrics
├── app.py                 # Streamlit web interface
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
└── README.md             # This file
```

## 🔧 Installation

### 1. Clone or Navigate to Project Directory

```bash
cd personalized_learning_buddy
```

### 2. Create Virtual Environment

```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your OpenAI API key
# OPENAI_API_KEY=your_actual_api_key_here
```

**Get your OpenAI API key**: https://platform.openai.com/api-keys

## 🎮 Usage

### Start the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## ☁️ Deploy on Streamlit Community Cloud

1. Push this project to a GitHub repository.
2. Go to https://share.streamlit.io/ and click **New app**.
3. Select your repo, set **Main file path** to `app.py`, and deploy.
4. In app settings, add this secret:

```toml
OPENAI_API_KEY="your_openai_api_key_here"
```

Notes:
- `runtime.txt` pins Python version for cloud runtime.
- `.streamlit/config.toml` is included for stable server/theme config.
- Dependencies install from `requirements.txt` with CPU-only PyTorch wheels.

### Workflow

1. **Upload Notes**: Go to "📄 Upload Notes" and upload your study materials (PDF/DOCX/TXT)
2. **Chat & Learn**: Ask questions about your notes in "💬 Chat & Learn"
3. **Take Quizzes**: Generate custom quizzes in "📝 Take Quiz"
4. **Track Progress**: View your performance in "📊 Performance"
5. **Get Study Plan**: Get personalized recommendations in "📅 Study Plan"

## 👥 Team Responsibilities

### Person 1: RAG + Embeddings (rag_pipeline.py)
- ✅ Document preprocessing (PDF/DOCX → text)
- ✅ Embedding creation using SentenceTransformers
- ✅ FAISS vector storage
- ✅ Retrieval pipeline implementation

### Person 2: Quiz Generation + Evaluation (quiz_generator.py, evaluate.py)
- ✅ MCQ, True/False, Short Answer generation
- ✅ Performance metrics tracking
- ✅ Topic-wise analysis
- ✅ Study plan generation

### Person 3: Web UI (app.py)
- ✅ Streamlit interface
- ✅ File upload functionality
- ✅ Chat interface
- ✅ Quiz dashboard
- ✅ Performance visualization

## 🧪 Testing Individual Components

### Test RAG Pipeline

```bash
python rag_pipeline.py
```

### Test Quiz Generator

```bash
python quiz_generator.py
```

### Test Evaluator

```bash
python evaluate.py
```

## 📊 Features Explained

### RAG (Retrieval-Augmented Generation)
- Splits documents into chunks
- Builds a TF-IDF index from notes
- Uses cosine similarity for relevant chunk retrieval
- Retrieves top-k relevant chunks for user queries

### Quiz Generation
- Uses retrieved context from RAG
- Generates diverse question types
- Provides explanations for answers
- Adapts difficulty based on performance

### Performance Tracking
- Records every quiz attempt
- Calculates accuracy metrics
- Identifies weak areas
- Generates personalized study plans

## 🔮 Future Enhancements

- [ ] Adaptive difficulty adjustment
- [ ] Voice-based Q&A
- [ ] Daily revision reminders via email
- [ ] Gamified leaderboard
- [ ] Spaced repetition algorithm
- [ ] Mobile app version
- [ ] Multi-language support
- [ ] Collaborative study groups

## 🐛 Troubleshooting

### Issue: "OpenAI API key not found"
**Solution**: Make sure you've created a `.env` file and added your API key:
```
OPENAI_API_KEY=sk-...your-key-here...
```

### Issue: "No module named 'sentence_transformers'"
**Solution**: Reinstall requirements:
```bash
pip install -r requirements.txt
```

### Issue: PDF text extraction fails
**Solution**: Try re-saving your PDF or use a different PDF reader to export it

### Issue: "FAISS index is empty"
**Solution**: Upload and process documents first before asking questions or generating quizzes

## 📝 Sample Usage

1. Upload a PDF about "Photosynthesis"
2. Ask: "Explain the light-dependent reactions"
3. Generate a quiz on "Photosynthesis"
4. Take the quiz and see your score
5. View your performance dashboard
6. Get a personalized study plan

## 🤝 Contributing

Feel free to fork this project and add your own features! Some ideas:
- Integration with other LLM providers (Anthropic, Cohere)
- Support for more document types (PowerPoint, images)
- Advanced analytics and insights
- Export quizzes to PDF

## 📄 License

This project is open source and available under the MIT License.

## 💡 Tips for Best Results

1. **Upload Quality Notes**: Clear, well-structured notes work best
2. **Specific Topics**: Focus quizzes on specific topics for better questions
3. **Regular Practice**: Take quizzes regularly to track progress
4. **Review Mistakes**: Always review incorrect answers
5. **Follow Study Plan**: Use the generated study plan consistently

---

**Built with ❤️ for better learning**

Happy Studying! 🎓✨
