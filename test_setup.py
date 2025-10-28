"""
Test script to verify all components are working
Run this after installation to check if everything is set up correctly
"""

import sys
import os

def test_imports():
    """Test if all required packages are installed"""
    print("🧪 Testing imports...")
    
    required_modules = [
        'streamlit',
        'sentence_transformers',
        'faiss',
        'PyPDF2',
        'docx',
        'pdfplumber',
        'langchain',
        'openai',
        'pandas',
        'plotly',
        'numpy'
    ]
    
    failed = []
    for module in required_modules:
        try:
            __import__(module)
            print(f"  ✅ {module}")
        except ImportError:
            print(f"  ❌ {module}")
            failed.append(module)
    
    if failed:
        print(f"\n❌ Failed to import: {', '.join(failed)}")
        print("Run: pip install -r requirements.txt")
        return False
    else:
        print("\n✅ All imports successful!")
        return True


def test_rag_pipeline():
    """Test RAG pipeline initialization"""
    print("\n🧪 Testing RAG Pipeline...")
    try:
        from rag_pipeline import RAGPipeline
        rag = RAGPipeline()
        print(f"  ✅ RAG Pipeline initialized (embedding dim: {rag.embedding_dim})")
        return True
    except Exception as e:
        print(f"  ❌ RAG Pipeline failed: {e}")
        return False


def test_quiz_generator():
    """Test Quiz Generator initialization"""
    print("\n🧪 Testing Quiz Generator...")
    try:
        from quiz_generator import QuizGenerator
        
        # Check for API key
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("  ⚠️  No OpenAI API key found (set in .env file)")
            print("  ℹ️  Quiz generator will not work without API key")
            return True
        
        quiz_gen = QuizGenerator(api_key)
        print("  ✅ Quiz Generator initialized")
        return True
    except Exception as e:
        print(f"  ❌ Quiz Generator failed: {e}")
        return False


def test_evaluator():
    """Test Evaluator initialization"""
    print("\n🧪 Testing Evaluator...")
    try:
        from evaluate import QuizEvaluator
        evaluator = QuizEvaluator()
        stats = evaluator.get_overall_statistics()
        print(f"  ✅ Evaluator initialized (quizzes: {stats['total_quizzes']})")
        return True
    except Exception as e:
        print(f"  ❌ Evaluator failed: {e}")
        return False


def test_directories():
    """Test if required directories exist"""
    print("\n🧪 Testing directories...")
    
    dirs = ['data', 'embeddings']
    for dir_name in dirs:
        if os.path.exists(dir_name):
            print(f"  ✅ {dir_name}/ exists")
        else:
            os.makedirs(dir_name, exist_ok=True)
            print(f"  ✅ {dir_name}/ created")
    
    return True


def test_env_file():
    """Check if .env file exists"""
    print("\n🧪 Checking environment setup...")
    
    if os.path.exists('.env'):
        print("  ✅ .env file found")
        
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key and api_key != "your_openai_api_key_here":
            print("  ✅ OpenAI API key configured")
        else:
            print("  ⚠️  OpenAI API key not configured")
            print("     Edit .env file and add your API key")
    else:
        print("  ⚠️  .env file not found")
        print("     Copy .env.example to .env and add your API key")
        print("     cp .env.example .env")
    
    return True


def main():
    """Run all tests"""
    print("="*50)
    print("🚀 PERSONALIZED LEARNING BUDDY - TEST SUITE")
    print("="*50)
    
    results = []
    
    results.append(("Imports", test_imports()))
    results.append(("Directories", test_directories()))
    results.append(("Environment", test_env_file()))
    results.append(("RAG Pipeline", test_rag_pipeline()))
    results.append(("Quiz Generator", test_quiz_generator()))
    results.append(("Evaluator", test_evaluator()))
    
    print("\n" + "="*50)
    print("📊 TEST SUMMARY")
    print("="*50)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name:20s} {status}")
    
    all_passed = all(r[1] for r in results)
    
    print("\n" + "="*50)
    if all_passed:
        print("✅ ALL TESTS PASSED!")
        print("\nYou can now run the app:")
        print("  streamlit run app.py")
    else:
        print("❌ SOME TESTS FAILED")
        print("\nPlease fix the issues above before running the app.")
    print("="*50)


if __name__ == "__main__":
    main()
