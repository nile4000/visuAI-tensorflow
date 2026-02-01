import time
import random
from typing import List, Dict, Tuple
from models.schemas import Prediction


class OmniService:
    """
    OmniRL Vision-Language Model Service
    
    Currently using mock responses for testing.
    Will be replaced with actual trained OmniRL model.
    """
    
    def __init__(self, use_mock: bool = True):
        self.use_mock = use_mock
        self.model = None
        self.model_loaded = False
        
        # Cache for repeated queries
        self.cache: Dict[str, Tuple[str, float]] = {}
        
        if not use_mock:
            self._load_model()
    
    def _load_model(self):
        """Load the trained OmniRL model"""
        # TODO: Implement actual model loading
        # from transformers import AutoModelForCausalLM, AutoTokenizer
        # self.model = AutoModelForCausalLM.from_pretrained(model_path)
        # self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model_loaded = True
        print("Model loading placeholder - will implement after training")
    
    def generate_description(self, predictions: List[Prediction]) -> Tuple[str, float, List[str]]:
        """
        Generate natural language description from predictions
        
        Args:
            predictions: List of MobileNet predictions
            
        Returns:
            Tuple of (description, confidence, used_predictions)
        """
        start_time = time.time()
        
        if self.use_mock:
            description, confidence, used = self._mock_describe(predictions)
        else:
            description, confidence, used = self._generate_with_model(predictions)
        
        processing_time = time.time() - start_time
        return description, confidence, used, processing_time
    
    def answer_question(self, predictions: List[Prediction], question: str) -> Tuple[str, float]:
        """
        Answer a question about the image based on predictions
        
        Args:
            predictions: List of MobileNet predictions
            question: User's question
            
        Returns:
            Tuple of (answer, confidence)
        """
        start_time = time.time()
        
        # Create cache key
        cache_key = f"{question}::{','.join([p.className for p in predictions[:3]])}"
        
        if cache_key in self.cache:
            answer, confidence = self.cache[cache_key]
        elif self.use_mock:
            answer, confidence = self._mock_answer(predictions, question)
            self.cache[cache_key] = (answer, confidence)
        else:
            answer, confidence = self._answer_with_model(predictions, question)
            self.cache[cache_key] = (answer, confidence)
        
        processing_time = time.time() - start_time
        return answer, confidence, processing_time
    
    # ==================== MOCK IMPLEMENTATIONS ====================
    
    def _mock_describe(self, predictions: List[Prediction]) -> Tuple[str, float, List[str]]:
        """Generate mock description for testing"""
        
        # Take top 3 predictions
        top_predictions = predictions[:3]
        used_classes = [p.className for p in top_predictions]
        
        # Generate description based on top prediction
        top_class = top_predictions[0].className
        top_prob = top_predictions[0].probability
        
        # Simple templates for common classes
        templates = {
            "laptop": [
                "A laptop computer is visible in the image.",
                "The image shows a laptop, possibly being used for work.",
                "A modern laptop can be seen in this picture."
            ],
            "cat": [
                "A cat is present in the image.",
                "The image features a cat, likely relaxing or playing.",
                "A feline companion can be seen in this picture."
            ],
            "dog": [
                "A dog is visible in the image.",
                "The image shows a dog, possibly a pet or companion animal.",
                "A canine friend can be seen in this picture."
            ],
            "person": [
                "A person is present in the image.",
                "The image features a person engaged in some activity.",
                "An individual can be seen in this picture."
            ],
            "car": [
                "A car is visible in the image.",
                "The image shows an automobile, possibly parked or in motion.",
                "A vehicle can be seen in this picture."
            ]
        }
        
        # Try to find matching template
        for key in templates:
            if key in top_class.lower():
                description = random.choice(templates[key])
                break
        else:
            # Generic template
            description = f"The image appears to show {top_class.replace('_', ' ')}"
            if len(top_predictions) > 1:
                secondary = top_predictions[1].className.replace('_', ' ')
                description += f", with {secondary} also present"
            description += "."
        
        # Confidence based on top prediction probability
        confidence = min(top_prob * 0.9, 0.95)  # Cap at 95%
        
        return description, confidence, used_classes
    
    def _mock_answer(self, predictions: List[Prediction], question: str) -> Tuple[str, float]:
        """Generate mock answer for testing"""
        
        question_lower = question.lower()
        top_class = predictions[0].className
        top_prob = predictions[0].probability
        
        # Question type detection
        if any(word in question_lower for word in ["what", "which", "identify"]):
            if "animal" in question_lower:
                # Check if any prediction is an animal
                animals = ["cat", "dog", "bird", "horse", "elephant", "tiger", "lion"]
                for pred in predictions:
                    for animal in animals:
                        if animal in pred.className.lower():
                            return f"The animal appears to be a {pred.className.replace('_', ' ')}.", pred.probability * 0.9
                return "I cannot identify a specific animal in this image.", 0.3
            
            elif "object" in question_lower or "see" in question_lower:
                return f"I can see {top_class.replace('_', ' ')} in the image.", top_prob * 0.85
            
            else:
                return f"The main subject appears to be {top_class.replace('_', ' ')}.", top_prob * 0.8
        
        elif any(word in question_lower for word in ["how many", "count"]):
            # Count questions
            return "Based on the predictions, there appears to be one main subject.", 0.6
        
        elif any(word in question_lower for word in ["is there", "are there", "can you see"]):
            # Yes/No questions
            # Check if question mentions any of the predicted classes
            for pred in predictions:
                if pred.className.lower() in question_lower or \
                   any(word in question_lower for word in pred.className.lower().split('_')):
                    return f"Yes, I can see {pred.className.replace('_', ' ')} in the image.", pred.probability * 0.9
            
            return "No, I cannot identify that in the image based on the available information.", 0.5
        
        elif any(word in question_lower for word in ["where", "location", "position"]):
            return "I can identify the object but cannot determine its exact position without spatial information.", 0.4
        
        elif any(word in question_lower for word in ["why", "reason"]):
            return "I can describe what's visible but cannot infer intent or reasoning.", 0.3
        
        else:
            # Generic answer
            return f"Based on the image, the main subject appears to be {top_class.replace('_', ' ')}.", top_prob * 0.7
    
    # ==================== REAL MODEL IMPLEMENTATIONS (TODO) ====================
    
    def _generate_with_model(self, predictions: List[Prediction]) -> Tuple[str, float, List[str]]:
        """Generate description using trained model"""
        # TODO: Implement after OmniRL training
        raise NotImplementedError("Model inference not yet implemented")
    
    def _answer_with_model(self, predictions: List[Prediction], question: str) -> Tuple[str, float]:
        """Answer question using trained model"""
        # TODO: Implement after OmniRL training
        raise NotImplementedError("Model inference not yet implemented")
