"""
Sample test data generator
Creates a sample document for testing the application
"""

def create_sample_notes():
    """Create sample study notes for testing"""
    
    content = """
# Introduction to Machine Learning

## What is Machine Learning?

Machine Learning (ML) is a subset of artificial intelligence that enables computers to learn and improve from experience without being explicitly programmed. It focuses on the development of computer programs that can access data and use it to learn for themselves.

## Types of Machine Learning

### 1. Supervised Learning
Supervised learning involves training a model on labeled data. The algorithm learns from the training data and applies that knowledge to new, unseen data. Common examples include:
- Classification (e.g., email spam detection)
- Regression (e.g., price prediction)

### 2. Unsupervised Learning
Unsupervised learning works with unlabeled data. The algorithm tries to find patterns and relationships in the data. Examples include:
- Clustering (e.g., customer segmentation)
- Dimensionality reduction (e.g., PCA)

### 3. Reinforcement Learning
Reinforcement learning involves an agent that learns to make decisions by interacting with an environment. The agent receives rewards or penalties based on its actions.

## Key Concepts

### Features and Labels
- **Features**: Input variables used to make predictions
- **Labels**: Output variables we want to predict

### Training and Testing
The dataset is typically split into:
- Training set (70-80%): Used to train the model
- Testing set (20-30%): Used to evaluate model performance

### Model Evaluation
Common metrics include:
- Accuracy: Percentage of correct predictions
- Precision: Ratio of true positives to predicted positives
- Recall: Ratio of true positives to actual positives
- F1 Score: Harmonic mean of precision and recall

## Popular Algorithms

### Linear Regression
Used for predicting continuous values. The algorithm finds the best-fitting line through the data points.

### Decision Trees
A tree-like model of decisions. Easy to interpret and visualize.

### Neural Networks
Inspired by biological neural networks. Capable of learning complex patterns in large datasets.

### Support Vector Machines (SVM)
Effective for classification tasks. Works by finding the optimal hyperplane that separates different classes.

## Applications of Machine Learning

1. **Healthcare**: Disease diagnosis, drug discovery
2. **Finance**: Fraud detection, stock prediction
3. **E-commerce**: Recommendation systems
4. **Autonomous Vehicles**: Self-driving cars
5. **Natural Language Processing**: Chatbots, translation

## Challenges in Machine Learning

### Overfitting
When a model performs well on training data but poorly on new data. Solutions include:
- Cross-validation
- Regularization
- Early stopping

### Underfitting
When a model is too simple to capture patterns in the data. Solutions:
- Increase model complexity
- Add more features
- Reduce regularization

### Data Quality
Poor quality data leads to poor model performance. Important considerations:
- Data cleaning
- Handling missing values
- Feature engineering

## Best Practices

1. Start with simple models
2. Always validate your model on unseen data
3. Monitor for bias in your data and models
4. Document your process and experiments
5. Continuously iterate and improve

## Conclusion

Machine Learning is a powerful tool that continues to evolve. Understanding the fundamentals and best practices is essential for building effective ML solutions.
"""
    
    return content


def save_sample_notes():
    """Save sample notes to a file"""
    import os
    
    # Create data directory if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Save as text file
    with open('data/sample_ml_notes.txt', 'w') as f:
        f.write(create_sample_notes())
    
    print("✅ Sample notes created: data/sample_ml_notes.txt")
    print("📝 You can now upload this file in the app to test the functionality!")


if __name__ == "__main__":
    save_sample_notes()
