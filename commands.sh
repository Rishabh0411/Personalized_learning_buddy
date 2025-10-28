#!/bin/bash

# Quick Commands Reference for Personalized Learning Buddy
# Copy and paste these commands as needed

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║     🧠 PERSONALIZED LEARNING BUDDY - QUICK COMMANDS          ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Navigate to project
echo "📁 Navigate to project:"
echo "   cd '/home/rishabh/Desktop/Projects/Gen AI Project/personalized_learning_buddy'"
echo ""

# Quick start
echo "🚀 Quick Start (Recommended):"
echo "   ./start.sh"
echo ""

# Manual setup
echo "🔧 Manual Setup:"
echo "   python3 -m venv venv"
echo "   source venv/bin/activate"
echo "   pip install --upgrade pip"
echo "   pip install -r requirements.txt"
echo "   cp .env.example .env"
echo "   # Edit .env and add your OpenAI API key"
echo "   nano .env"
echo ""

# Create sample data
echo "📝 Create Sample Test Data:"
echo "   python create_sample_data.py"
echo ""

# Run tests
echo "🧪 Run Setup Tests:"
echo "   python test_setup.py"
echo ""

# Start application
echo "▶️  Start Application:"
echo "   streamlit run app.py"
echo ""

# Alternative port
echo "🔄 Start on Different Port:"
echo "   streamlit run app.py --server.port 8502"
echo ""

# Test individual components
echo "🧩 Test Individual Components:"
echo "   python -c 'from rag_pipeline import RAGPipeline; r = RAGPipeline(); print(\"RAG OK\")'"
echo "   python -c 'from quiz_generator import QuizGenerator; print(\"Quiz Gen OK\")'"
echo "   python -c 'from evaluate import QuizEvaluator; e = QuizEvaluator(); print(\"Eval OK\")'"
echo ""

# Check versions
echo "📋 Check Versions:"
echo "   python3 --version"
echo "   pip --version"
echo "   streamlit --version"
echo ""

# Verify API key
echo "🔑 Verify API Key:"
echo "   python -c 'from dotenv import load_dotenv; import os; load_dotenv(); print(\"API Key:\", \"Found\" if os.getenv(\"OPENAI_API_KEY\") else \"NOT FOUND\")'"
echo ""

# View logs
echo "📜 View Logs:"
echo "   tail -f ~/.streamlit/logs/streamlit.log"
echo ""

# Clean up
echo "🧹 Clean Up (if needed):"
echo "   rm -rf venv/"
echo "   rm -rf embeddings/vectorstore.pkl"
echo "   rm data/quiz_results.json"
echo ""

# Update dependencies
echo "⬆️  Update Dependencies:"
echo "   pip install --upgrade -r requirements.txt"
echo ""

# Git commands (if using git)
echo "📦 Git Commands:"
echo "   git init"
echo "   git add ."
echo "   git commit -m 'Initial commit: Personalized Learning Buddy'"
echo ""

# Open in browser
echo "🌐 Open in Browser:"
echo "   http://localhost:8501"
echo ""

# Get help
echo "❓ Get Help:"
echo "   cat README.md"
echo "   cat QUICKSTART.md"
echo "   cat TROUBLESHOOTING.md"
echo ""

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    🎯 READY TO START?                        ║"
echo "╠══════════════════════════════════════════════════════════════╣"
echo "║  1. Run: ./start.sh                                          ║"
echo "║  2. Add OpenAI API key to .env file                          ║"
echo "║  3. Open browser at http://localhost:8501                    ║"
echo "║  4. Upload sample_ml_notes.txt from data/ folder             ║"
echo "║  5. Start learning! 🚀                                       ║"
echo "╚══════════════════════════════════════════════════════════════╝"
