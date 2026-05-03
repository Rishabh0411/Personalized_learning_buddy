"""
Streamlit Web Application - Person 3's Component
Main interface for the Personalized Learning Buddy
"""

import streamlit as st
import os
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from rag_pipeline import RAGPipeline
from quiz_generator import QuizGenerator
from evaluate import QuizEvaluator


# Page configuration
st.set_page_config(
    page_title="Personalized Learning Buddy",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #ff7f0e;
        margin-top: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
    .success-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
    }
    .info-box {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #d1ecf1;
        border: 1px solid #bee5eb;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'rag_pipeline' not in st.session_state:
    st.session_state.rag_pipeline = None
if 'quiz_generator' not in st.session_state:
    st.session_state.quiz_generator = None
if 'evaluator' not in st.session_state:
    st.session_state.evaluator = QuizEvaluator()
if 'current_quiz' not in st.session_state:
    st.session_state.current_quiz = None
if 'quiz_answers' not in st.session_state:
    st.session_state.quiz_answers = {}
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'documents_loaded' not in st.session_state:
    st.session_state.documents_loaded = False


def get_openai_api_key():
    """Read OpenAI key from Streamlit secrets first, then environment."""
    if "OPENAI_API_KEY" in st.secrets:
        return st.secrets["OPENAI_API_KEY"]
    return os.getenv("OPENAI_API_KEY")


def initialize_components():
    """Initialize RAG pipeline and Quiz Generator"""
    try:
        if st.session_state.rag_pipeline is None:
            with st.spinner("Initializing RAG Pipeline..."):
                st.session_state.rag_pipeline = RAGPipeline()
                # Try to load existing vectorstore
                st.session_state.rag_pipeline.load_vectorstore()
        
        if st.session_state.quiz_generator is None:
            api_key = get_openai_api_key()
            if api_key:
                with st.spinner("Initializing Quiz Generator..."):
                    st.session_state.quiz_generator = QuizGenerator(api_key)
            else:
                st.warning("⚠️ OpenAI API key not found. Set OPENAI_API_KEY in .env (local) or Streamlit Secrets (deployment).")
        
        return True
    except Exception as e:
        st.error(f"Error initializing components: {e}")
        return False


def upload_documents_page():
    """Document upload interface"""
    st.markdown("<h2 class='sub-header'>📄 Upload Your Study Notes</h2>", unsafe_allow_html=True)
    
    st.write("Upload your notes in PDF, DOCX, or TXT format to get started!")
    
    uploaded_files = st.file_uploader(
        "Choose files",
        type=['pdf', 'docx', 'txt'],
        accept_multiple_files=True,
        help="Upload multiple files at once"
    )
    
    if uploaded_files:
        if st.button("🚀 Process Documents", type="primary"):
            try:
                # Save uploaded files
                for uploaded_file in uploaded_files:
                    file_path = os.path.join("data", uploaded_file.name)
                    with open(file_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                
                # Process documents
                with st.spinner("Processing documents and creating embeddings..."):
                    for uploaded_file in uploaded_files:
                        file_path = os.path.join("data", uploaded_file.name)
                        documents = st.session_state.rag_pipeline.process_document(file_path)
                        st.session_state.rag_pipeline.build_index(documents)
                    
                    # Save vectorstore
                    st.session_state.rag_pipeline.save_vectorstore()
                    st.session_state.documents_loaded = True
                
                st.success(f"✅ Successfully processed {len(uploaded_files)} document(s)!")
                st.balloons()
                
            except Exception as e:
                st.error(f"Error processing documents: {e}")


def chat_interface_page():
    """Chat interface for asking questions"""
    st.markdown("<h2 class='sub-header'>💬 Ask Questions About Your Notes</h2>", unsafe_allow_html=True)
    
    if not st.session_state.documents_loaded:
        st.warning("⚠️ Please upload and process documents first!")
        return
    
    # Display chat history
    chat_container = st.container()
    
    with chat_container:
        for i, message in enumerate(st.session_state.chat_history):
            if message['role'] == 'user':
                st.markdown(f"**🧑 You:** {message['content']}")
            else:
                st.markdown(f"**🤖 Buddy:** {message['content']}")
            st.markdown("---")
    
    # Chat input
    user_question = st.text_input("Ask a question:", key="chat_input")
    
    col1, col2 = st.columns([1, 5])
    with col1:
        ask_button = st.button("Ask", type="primary")
    with col2:
        clear_button = st.button("Clear Chat")
    
    if clear_button:
        st.session_state.chat_history = []
        st.rerun()
    
    if ask_button and user_question:
        # Get context from RAG
        context = st.session_state.rag_pipeline.get_context_for_query(user_question, top_k=3)
        
        if not context:
            response = "I couldn't find relevant information in your notes. Try uploading more documents or rephrasing your question."
        else:
            # Generate explanation using quiz generator
            if st.session_state.quiz_generator:
                response = st.session_state.quiz_generator.explain_concept(context, user_question)
            else:
                response = f"**Context from your notes:**\n\n{context}"
        
        # Add to chat history
        st.session_state.chat_history.append({'role': 'user', 'content': user_question})
        st.session_state.chat_history.append({'role': 'assistant', 'content': response})
        
        st.rerun()


def quiz_generation_page():
    """Quiz generation interface"""
    st.markdown("<h2 class='sub-header'>📝 Generate Quiz</h2>", unsafe_allow_html=True)
    
    if not st.session_state.documents_loaded:
        st.warning("⚠️ Please upload and process documents first!")
        return
    
    if not st.session_state.quiz_generator:
        st.error("⚠️ Quiz generator not initialized. Configure OPENAI_API_KEY in .env (local) or Streamlit Secrets (deployment).")
        return
    
    # Quiz configuration
    col1, col2 = st.columns(2)
    
    with col1:
        quiz_topic = st.text_input("Quiz Topic/Focus:", placeholder="e.g., Chapter 1, Photosynthesis, etc.")
        num_mcq = st.slider("Number of Multiple Choice Questions", 0, 10, 3)
        num_tf = st.slider("Number of True/False Questions", 0, 10, 3)
    
    with col2:
        num_short = st.slider("Number of Short Answer Questions", 0, 5, 2)
        difficulty = st.select_slider("Difficulty Level", options=["Easy", "Medium", "Hard"], value="Medium")
    
    if st.button("🎯 Generate Quiz", type="primary"):
        with st.spinner("Generating quiz questions..."):
            try:
                # Get relevant context based on topic
                context = st.session_state.rag_pipeline.get_context_for_query(
                    quiz_topic if quiz_topic else "general topics",
                    top_k=5
                )
                
                if not context:
                    st.error("Could not retrieve relevant content. Please try a different topic.")
                    return
                
                # Generate quiz
                quiz_questions = st.session_state.quiz_generator.generate_mixed_quiz(
                    context,
                    num_mcq=num_mcq,
                    num_tf=num_tf,
                    num_short=num_short
                )
                
                if quiz_questions:
                    st.session_state.current_quiz = {
                        'id': f"quiz_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                        'topic': quiz_topic if quiz_topic else "General",
                        'questions': quiz_questions
                    }
                    st.session_state.quiz_answers = {}
                    st.success("✅ Quiz generated successfully! Scroll down to take the quiz.")
                else:
                    st.error("Failed to generate quiz. Please try again.")
                
            except Exception as e:
                st.error(f"Error generating quiz: {e}")
    
    # Display current quiz
    if st.session_state.current_quiz:
        st.markdown("---")
        st.markdown(f"### 📋 Quiz: {st.session_state.current_quiz['topic']}")
        
        questions = st.session_state.current_quiz['questions']
        
        for i, question in enumerate(questions, 1):
            st.markdown(f"**Question {i}:** {question['question']}")
            
            if question['type'] == 'mcq':
                answer = st.radio(
                    "Select your answer:",
                    question['options'],
                    key=f"q_{i}",
                    index=None
                )
                if answer:
                    st.session_state.quiz_answers[i] = answer[0]  # Store just the letter
            
            elif question['type'] == 'true_false':
                answer = st.radio(
                    "Select your answer:",
                    ["True", "False"],
                    key=f"q_{i}",
                    index=None
                )
                if answer:
                    st.session_state.quiz_answers[i] = answer
            
            elif question['type'] == 'short_answer':
                answer = st.text_area(
                    "Your answer:",
                    key=f"q_{i}",
                    height=100
                )
                if answer:
                    st.session_state.quiz_answers[i] = answer
            
            st.markdown("---")
        
        if st.button("✅ Submit Quiz", type="primary"):
            if len(st.session_state.quiz_answers) < len(questions):
                st.warning("⚠️ Please answer all questions before submitting!")
            else:
                # Prepare answers list
                answers = [st.session_state.quiz_answers.get(i+1, "") for i in range(len(questions))]
                
                # Record quiz attempt
                result = st.session_state.evaluator.record_quiz_attempt(
                    st.session_state.current_quiz['id'],
                    questions,
                    answers,
                    st.session_state.current_quiz['topic']
                )
                
                # Display results
                st.success(f"🎉 Quiz completed! Your score: {result['accuracy']}%")
                st.write(f"Correct: {result['correct_answers']}/{result['total_questions']}")
                
                # Show detailed results
                with st.expander("📊 View Detailed Results"):
                    for detail in result['detailed_results']:
                        if detail['is_correct']:
                            st.success(f"✅ Question {detail['question_num']}: Correct!")
                        else:
                            st.error(f"❌ Question {detail['question_num']}: Incorrect")
                            st.write(f"Your answer: {detail['user_answer']}")
                            st.write(f"Correct answer: {detail['correct_answer']}")
                
                # Clear current quiz
                st.session_state.current_quiz = None
                st.session_state.quiz_answers = {}


def performance_dashboard_page():
    """Performance tracking and visualization"""
    st.markdown("<h2 class='sub-header'>📊 Your Performance Dashboard</h2>", unsafe_allow_html=True)
    
    evaluator = st.session_state.evaluator
    overall_stats = evaluator.get_overall_statistics()
    
    if overall_stats['total_quizzes'] == 0:
        st.info("📝 No quiz data yet. Take some quizzes to see your performance!")
        return
    
    # Overall Statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Quizzes", overall_stats['total_quizzes'])
    with col2:
        st.metric("Average Accuracy", f"{overall_stats['average_accuracy']}%")
    with col3:
        st.metric("Total Questions", overall_stats['total_questions'])
    with col4:
        st.metric("Success Rate", f"{overall_stats['success_rate']}%")
    
    st.markdown("---")
    
    # Performance over time
    df = evaluator.export_to_dataframe()
    if not df.empty:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📈 Accuracy Trend")
            fig = px.line(df, x='timestamp', y='accuracy', 
                         title='Quiz Accuracy Over Time',
                         markers=True)
            fig.update_layout(xaxis_title="Date", yaxis_title="Accuracy (%)")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown("### 📊 Topic Performance")
            topic_perf = evaluator.get_topic_performance()
            if topic_perf:
                topics = list(topic_perf.keys())
                accuracies = [topic_perf[t]['average_accuracy'] for t in topics]
                
                fig = go.Figure(data=[go.Bar(x=topics, y=accuracies)])
                fig.update_layout(
                    title='Average Accuracy by Topic',
                    xaxis_title="Topic",
                    yaxis_title="Accuracy (%)",
                    yaxis_range=[0, 100]
                )
                st.plotly_chart(fig, use_container_width=True)
    
    # Recent Performance
    st.markdown("### 🕐 Recent Quizzes")
    recent = evaluator.get_recent_performance(5)
    
    if recent:
        for quiz in reversed(recent):
            with st.expander(f"📝 {quiz['topic']} - {quiz['timestamp'][:10]} (Score: {quiz['accuracy']}%)"):
                st.write(f"**Questions:** {quiz['total_questions']}")
                st.write(f"**Correct:** {quiz['correct_answers']}")
                st.write(f"**Incorrect:** {quiz['incorrect_answers']}")


def study_plan_page():
    """Personalized study plan generation"""
    st.markdown("<h2 class='sub-header'>📅 Personalized Study Plan</h2>", unsafe_allow_html=True)
    
    evaluator = st.session_state.evaluator
    
    if evaluator.get_overall_statistics()['total_quizzes'] == 0:
        st.info("📝 Complete some quizzes first to get a personalized study plan!")
        return
    
    # Generate study plan
    study_plan = evaluator.generate_study_plan()
    
    st.markdown(f"""
    <div class='info-box'>
    <pre>{study_plan}</pre>
    </div>
    """, unsafe_allow_html=True)
    
    # Weak areas
    weak_areas = evaluator.get_weak_areas()
    
    if weak_areas:
        st.markdown("### 🎯 Focus Areas")
        st.warning("These topics need more attention:")
        for area in weak_areas:
            st.write(f"- {area}")
    else:
        st.success("🎉 Great job! You're performing well across all topics!")


def main():
    """Main application"""
    
    # Header
    st.markdown("<h1 class='main-header'>🧠 Personalized Learning Buddy</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666;'>Your AI-powered study companion for smarter learning</p>", unsafe_allow_html=True)
    
    # Initialize components
    initialize_components()
    
    # Sidebar navigation
    st.sidebar.title("🧭 Navigation")
    page = st.sidebar.radio(
        "Go to:",
        ["📄 Upload Notes", "💬 Chat & Learn", "📝 Take Quiz", "📊 Performance", "📅 Study Plan"]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📚 Quick Stats")
    stats = st.session_state.evaluator.get_overall_statistics()
    st.sidebar.metric("Quizzes Taken", stats['total_quizzes'])
    if stats['total_quizzes'] > 0:
        st.sidebar.metric("Average Score", f"{stats['average_accuracy']}%")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### ℹ️ About")
    st.sidebar.info(
        "This app uses RAG + LLM to help you study smarter. "
        "Upload your notes, ask questions, take quizzes, and track your progress!"
    )
    
    # Route to pages
    if page == "📄 Upload Notes":
        upload_documents_page()
    elif page == "💬 Chat & Learn":
        chat_interface_page()
    elif page == "📝 Take Quiz":
        quiz_generation_page()
    elif page == "📊 Performance":
        performance_dashboard_page()
    elif page == "📅 Study Plan":
        study_plan_page()


if __name__ == "__main__":
    main()
