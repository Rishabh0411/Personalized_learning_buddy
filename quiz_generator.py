"""
Quiz Generator - Person 2's Component
Generates quizzes using LLM and retrieved content from RAG
"""

import json
import os
from typing import List, Dict, Any
from datetime import datetime
import openai
from dotenv import load_dotenv

load_dotenv()

class QuizGenerator:
    """
    Generate different types of quiz questions using LLM
    """
    
    def __init__(self, api_key: str = None):
        """
        Initialize Quiz Generator with OpenAI API
        
        Args:
            api_key: OpenAI API key (optional, can use env variable)
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set OPENAI_API_KEY in .env file")
        
        openai.api_key = self.api_key
        self.client = openai.OpenAI(api_key=self.api_key)
    
    def generate_mcqs(self, context: str, num_questions: int = 5) -> List[Dict[str, Any]]:
        """
        Generate Multiple Choice Questions from context
        
        Args:
            context: Text context from retrieved documents
            num_questions: Number of MCQs to generate
            
        Returns:
            List of MCQ dictionaries
        """
        prompt = f"""Based on the following text, generate {num_questions} multiple choice questions.

Text:
{context}

Generate questions in the following JSON format:
[
  {{
    "question": "Question text here?",
    "options": ["A) Option 1", "B) Option 2", "C) Option 3", "D) Option 4"],
    "correct_answer": "A",
    "explanation": "Brief explanation of why this is correct"
  }}
]

Make sure the questions test understanding, not just memorization. Return ONLY valid JSON."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert educator who creates challenging and fair quiz questions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            content = response.choices[0].message.content.strip()
            
            # Extract JSON from response
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            questions = json.loads(content)
            
            # Add metadata
            for q in questions:
                q['type'] = 'mcq'
                q['timestamp'] = datetime.now().isoformat()
            
            return questions
            
        except Exception as e:
            print(f"Error generating MCQs: {e}")
            return []
    
    def generate_true_false(self, context: str, num_questions: int = 5) -> List[Dict[str, Any]]:
        """
        Generate True/False Questions from context
        
        Args:
            context: Text context from retrieved documents
            num_questions: Number of T/F questions to generate
            
        Returns:
            List of True/False question dictionaries
        """
        prompt = f"""Based on the following text, generate {num_questions} true/false questions.

Text:
{context}

Generate questions in the following JSON format:
[
  {{
    "question": "Statement to evaluate",
    "correct_answer": "True" or "False",
    "explanation": "Brief explanation"
  }}
]

Return ONLY valid JSON."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert educator who creates clear true/false questions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content.strip()
            
            # Extract JSON from response
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            questions = json.loads(content)
            
            # Add metadata
            for q in questions:
                q['type'] = 'true_false'
                q['timestamp'] = datetime.now().isoformat()
            
            return questions
            
        except Exception as e:
            print(f"Error generating True/False questions: {e}")
            return []
    
    def generate_short_answer(self, context: str, num_questions: int = 3) -> List[Dict[str, Any]]:
        """
        Generate Short Answer Questions from context
        
        Args:
            context: Text context from retrieved documents
            num_questions: Number of short answer questions to generate
            
        Returns:
            List of short answer question dictionaries
        """
        prompt = f"""Based on the following text, generate {num_questions} short answer questions.

Text:
{context}

Generate questions in the following JSON format:
[
  {{
    "question": "Question requiring a short answer?",
    "sample_answer": "A good sample answer",
    "key_points": ["point 1", "point 2", "point 3"]
  }}
]

Return ONLY valid JSON."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert educator who creates thoughtful short answer questions."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content.strip()
            
            # Extract JSON from response
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
            
            questions = json.loads(content)
            
            # Add metadata
            for q in questions:
                q['type'] = 'short_answer'
                q['timestamp'] = datetime.now().isoformat()
            
            return questions
            
        except Exception as e:
            print(f"Error generating short answer questions: {e}")
            return []
    
    def generate_mixed_quiz(self, context: str, num_mcq: int = 3, num_tf: int = 3, num_short: int = 2) -> List[Dict[str, Any]]:
        """
        Generate a mixed quiz with different question types
        
        Args:
            context: Text context from retrieved documents
            num_mcq: Number of MCQs
            num_tf: Number of True/False questions
            num_short: Number of short answer questions
            
        Returns:
            List of mixed question dictionaries
        """
        all_questions = []
        
        if num_mcq > 0:
            mcqs = self.generate_mcqs(context, num_mcq)
            all_questions.extend(mcqs)
        
        if num_tf > 0:
            tfs = self.generate_true_false(context, num_tf)
            all_questions.extend(tfs)
        
        if num_short > 0:
            shorts = self.generate_short_answer(context, num_short)
            all_questions.extend(shorts)
        
        return all_questions
    
    def explain_concept(self, context: str, concept: str) -> str:
        """
        Generate explanation for a difficult concept
        
        Args:
            context: Relevant text from documents
            concept: Concept to explain
            
        Returns:
            Detailed explanation
        """
        prompt = f"""Based on the following context, explain the concept '{concept}' in a clear and engaging way.

Context:
{context}

Provide:
1. A simple definition
2. An analogy or example
3. Key points to remember
4. Common misconceptions (if any)

Make it easy to understand for a student."""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert teacher who explains concepts clearly with examples."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )
            
            explanation = response.choices[0].message.content.strip()
            return explanation
            
        except Exception as e:
            print(f"Error generating explanation: {e}")
            return "Could not generate explanation at this time."


# Test function
if __name__ == "__main__":
    # Example usage (requires API key)
    try:
        quiz_gen = QuizGenerator()
        print("Quiz Generator initialized successfully!")
    except Exception as e:
        print(f"Error: {e}")
        print("Please set OPENAI_API_KEY in .env file")
