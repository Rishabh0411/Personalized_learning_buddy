"""
Evaluation Metrics - Person 2's Component
Track and analyze quiz performance
"""

import json
import os
from typing import List, Dict, Any
from datetime import datetime
from collections import defaultdict
import pandas as pd


class QuizEvaluator:
    """
    Evaluate quiz performance and track learning progress
    """
    
    def __init__(self, results_file: str = "data/quiz_results.json"):
        """
        Initialize Quiz Evaluator
        
        Args:
            results_file: Path to store quiz results
        """
        self.results_file = results_file
        self.results = self.load_results()
    
    def load_results(self) -> List[Dict[str, Any]]:
        """Load existing quiz results from file"""
        if os.path.exists(self.results_file):
            try:
                with open(self.results_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading results: {e}")
                return []
        return []
    
    def save_results(self):
        """Save quiz results to file"""
        os.makedirs(os.path.dirname(self.results_file), exist_ok=True)
        with open(self.results_file, 'w') as f:
            json.dump(self.results, f, indent=2)
    
    def record_quiz_attempt(self, 
                           quiz_id: str,
                           questions: List[Dict[str, Any]], 
                           answers: List[str],
                           topic: str = "General") -> Dict[str, Any]:
        """
        Record a quiz attempt and calculate metrics
        
        Args:
            quiz_id: Unique identifier for the quiz
            questions: List of question dictionaries
            answers: List of user answers
            topic: Topic/subject of the quiz
            
        Returns:
            Dictionary with performance metrics
        """
        correct_count = 0
        total_questions = len(questions)
        detailed_results = []
        
        for i, (question, user_answer) in enumerate(zip(questions, answers)):
            is_correct = False
            
            if question['type'] == 'mcq':
                correct_answer = question.get('correct_answer', '')
                is_correct = user_answer.upper() == correct_answer.upper()
            
            elif question['type'] == 'true_false':
                correct_answer = question.get('correct_answer', '')
                is_correct = user_answer.lower() == correct_answer.lower()
            
            elif question['type'] == 'short_answer':
                # For short answers, we'll mark as correct if provided
                # In a real system, you'd use semantic similarity or manual review
                is_correct = len(user_answer.strip()) > 10  # Basic check
            
            if is_correct:
                correct_count += 1
            
            detailed_results.append({
                'question_num': i + 1,
                'question': question.get('question', ''),
                'user_answer': user_answer,
                'correct_answer': question.get('correct_answer', question.get('sample_answer', '')),
                'is_correct': is_correct,
                'type': question['type']
            })
        
        # Calculate metrics
        accuracy = (correct_count / total_questions * 100) if total_questions > 0 else 0
        
        attempt_record = {
            'quiz_id': quiz_id,
            'timestamp': datetime.now().isoformat(),
            'topic': topic,
            'total_questions': total_questions,
            'correct_answers': correct_count,
            'incorrect_answers': total_questions - correct_count,
            'accuracy': round(accuracy, 2),
            'detailed_results': detailed_results
        }
        
        self.results.append(attempt_record)
        self.save_results()
        
        return attempt_record
    
    def get_overall_statistics(self) -> Dict[str, Any]:
        """
        Calculate overall performance statistics
        
        Returns:
            Dictionary with overall stats
        """
        if not self.results:
            return {
                'total_quizzes': 0,
                'total_questions': 0,
                'average_accuracy': 0,
                'total_correct': 0,
                'total_incorrect': 0
            }
        
        total_quizzes = len(self.results)
        total_questions = sum(r['total_questions'] for r in self.results)
        total_correct = sum(r['correct_answers'] for r in self.results)
        total_incorrect = sum(r['incorrect_answers'] for r in self.results)
        average_accuracy = sum(r['accuracy'] for r in self.results) / total_quizzes
        
        return {
            'total_quizzes': total_quizzes,
            'total_questions': total_questions,
            'average_accuracy': round(average_accuracy, 2),
            'total_correct': total_correct,
            'total_incorrect': total_incorrect,
            'success_rate': round((total_correct / total_questions * 100) if total_questions > 0 else 0, 2)
        }
    
    def get_topic_performance(self) -> Dict[str, Dict[str, Any]]:
        """
        Get performance breakdown by topic
        
        Returns:
            Dictionary with topic-wise performance
        """
        topic_stats = defaultdict(lambda: {'quizzes': 0, 'questions': 0, 'correct': 0, 'accuracy': []})
        
        for result in self.results:
            topic = result['topic']
            topic_stats[topic]['quizzes'] += 1
            topic_stats[topic]['questions'] += result['total_questions']
            topic_stats[topic]['correct'] += result['correct_answers']
            topic_stats[topic]['accuracy'].append(result['accuracy'])
        
        # Calculate averages
        topic_performance = {}
        for topic, stats in topic_stats.items():
            avg_accuracy = sum(stats['accuracy']) / len(stats['accuracy']) if stats['accuracy'] else 0
            topic_performance[topic] = {
                'quizzes_taken': stats['quizzes'],
                'total_questions': stats['questions'],
                'correct_answers': stats['correct'],
                'average_accuracy': round(avg_accuracy, 2)
            }
        
        return topic_performance
    
    def get_recent_performance(self, num_quizzes: int = 5) -> List[Dict[str, Any]]:
        """
        Get performance for recent quizzes
        
        Args:
            num_quizzes: Number of recent quizzes to retrieve
            
        Returns:
            List of recent quiz results
        """
        return self.results[-num_quizzes:] if self.results else []
    
    def get_weak_areas(self) -> List[str]:
        """
        Identify weak areas based on performance
        
        Returns:
            List of topics/areas that need improvement
        """
        topic_performance = self.get_topic_performance()
        weak_areas = []
        
        for topic, stats in topic_performance.items():
            if stats['average_accuracy'] < 60:  # Less than 60% accuracy
                weak_areas.append(f"{topic} (Accuracy: {stats['average_accuracy']}%)")
        
        return weak_areas
    
    def generate_study_plan(self) -> str:
        """
        Generate a personalized study plan based on performance
        
        Returns:
            Study plan as a string
        """
        if not self.results:
            return "Complete some quizzes first to generate a personalized study plan!"
        
        overall_stats = self.get_overall_statistics()
        weak_areas = self.get_weak_areas()
        topic_performance = self.get_topic_performance()
        
        plan = "📚 PERSONALIZED STUDY PLAN\n\n"
        plan += f"Overall Performance: {overall_stats['average_accuracy']}%\n"
        plan += f"Total Quizzes Completed: {overall_stats['total_quizzes']}\n\n"
        
        if overall_stats['average_accuracy'] >= 80:
            plan += "🎉 Excellent work! You're doing great!\n\n"
        elif overall_stats['average_accuracy'] >= 60:
            plan += "👍 Good progress! Keep it up!\n\n"
        else:
            plan += "💪 You can do this! Let's focus on improvement.\n\n"
        
        if weak_areas:
            plan += "🎯 Areas needing attention:\n"
            for area in weak_areas:
                plan += f"  - {area}\n"
            plan += "\n"
        
        plan += "📅 Recommended Study Schedule:\n"
        
        # Prioritize weak areas
        sorted_topics = sorted(topic_performance.items(), 
                             key=lambda x: x[1]['average_accuracy'])
        
        for i, (topic, stats) in enumerate(sorted_topics[:3], 1):
            plan += f"  {i}. {topic} - Review and practice (Current: {stats['average_accuracy']}%)\n"
        
        plan += "\n💡 Tips:\n"
        plan += "  - Review incorrect answers from previous quizzes\n"
        plan += "  - Take short breaks between study sessions\n"
        plan += "  - Focus on understanding concepts, not memorization\n"
        plan += "  - Retake quizzes on weak topics\n"
        
        return plan
    
    def export_to_dataframe(self) -> pd.DataFrame:
        """
        Export results to pandas DataFrame for analysis
        
        Returns:
            DataFrame with quiz results
        """
        if not self.results:
            return pd.DataFrame()
        
        flat_results = []
        for result in self.results:
            flat_results.append({
                'quiz_id': result['quiz_id'],
                'timestamp': result['timestamp'],
                'topic': result['topic'],
                'total_questions': result['total_questions'],
                'correct_answers': result['correct_answers'],
                'accuracy': result['accuracy']
            })
        
        return pd.DataFrame(flat_results)


# Test function
if __name__ == "__main__":
    evaluator = QuizEvaluator()
    print("Quiz Evaluator initialized successfully!")
    stats = evaluator.get_overall_statistics()
    print(f"Overall Statistics: {stats}")
