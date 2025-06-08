#!/usr/bin/env python3
# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "requests",
# ]
# ///
"""
AI Feedback System Test Script

This script tests the complete AI feedback pipeline including:
- Creating test quiz data
- Making quiz attempts with responses
- Generating AI feedback
- Testing all API endpoints
- Cleanup functionality

Usage:
    python test_ai_feedback.py --test-all
    python test_ai_feedback.py --create-test-data
    python test_ai_feedback.py --test-feedback --response-id 28
    python test_ai_feedback.py --cleanup
"""

import argparse
import json
import time
import requests
from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class TestConfig:
    """Configuration for test environment"""
    backend_url: str = "https://quized.dashgin.com"
    ai_service_url: str = "https://quized.dashgin.com/"
    # Replace with your actual token
    access_token: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3NDk5MjUwNTksInN1YiI6IjcifQ.5jGJ0tExl74ET_n3N2wqWhRy4h9WVyYDCuPqI4DFqqY"
    
    @property
    def headers(self) -> Dict[str, str]:
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }


class AIFeedbackTester:
    """Test suite for AI feedback system"""
    
    def __init__(self, config: TestConfig):
        self.config = config
        self.created_resources = {
            "questions": [],
            "attempts": [],
            "responses": [],
            "feedback": []
        }
    
    def test_health_check(self) -> bool:
        """Test if backend and AI service are running"""
        print("🔍 Testing service health...")
        
        # Test backend
        try:
            response = requests.get(f"{self.config.backend_url}/api/v1/utils/health-check")
            backend_healthy = response.status_code == 200
            print(f"  Backend: {'✅ Healthy' if backend_healthy else '❌ Unhealthy'}")
        except Exception as e:
            print(f"  Backend: ❌ Error - {e}")
            backend_healthy = False
        
        # Test AI service
        try:
            response = requests.get(f"{self.config.ai_service_url}/ai-api/health")
            ai_healthy = response.status_code == 200
            print(f"  AI Service: {'✅ Healthy' if ai_healthy else '❌ Unhealthy'}")
        except Exception as e:
            print(f"  AI Service: ❌ Error - {e}")
            ai_healthy = False
        
        return backend_healthy and ai_healthy
    
    def create_test_question(self, quiz_id: int = 2) -> Optional[int]:
        """Create a test question for AI feedback testing"""
        print(f"📝 Creating test question for quiz {quiz_id}...")
        
        question_data = {
            "quiz_id": quiz_id,
            "text": "Explain what a programming language is and give three examples.",
            "question_type": "text",
            "order_position": 1,
            "model_answer": "A programming language is a formal language comprising a set of instructions that can be used to produce various kinds of output. Examples include Python, Java, and JavaScript.",
            "key_concepts": {
                "concepts": ["programming language", "formal language", "instructions", "output", "examples"]
            }
        }
        
        try:
            response = requests.post(
                f"{self.config.backend_url}/api/v1/questions/",
                headers=self.config.headers,
                data=json.dumps(question_data)
            )
            
            if response.status_code == 201:
                question_id = response.json()["id"]
                self.created_resources["questions"].append(question_id)
                print(f"  ✅ Created question ID: {question_id}")
                return question_id
            else:
                print(f"  ❌ Failed to create question: {response.text}")
                return None
                
        except Exception as e:
            print(f"  ❌ Error creating question: {e}")
            return None
    
    def create_test_attempt(self, quiz_id: int = 2) -> Optional[int]:
        """Create a test quiz attempt"""
        print(f"🎯 Creating test attempt for quiz {quiz_id}...")
        
        attempt_data = {
            "quiz_id": quiz_id,
            "is_completed": False
        }
        
        try:
            response = requests.post(
                f"{self.config.backend_url}/api/v1/attempts/",
                headers=self.config.headers,
                data=json.dumps(attempt_data)
            )
            
            if response.status_code == 201:
                attempt_id = response.json()["id"]
                self.created_resources["attempts"].append(attempt_id)
                print(f"  ✅ Created attempt ID: {attempt_id}")
                return attempt_id
            else:
                print(f"  ❌ Failed to create attempt: {response.text}")
                return None
                
        except Exception as e:
            print(f"  ❌ Error creating attempt: {e}")
            return None
    
    def create_test_response(self, attempt_id: int, question_id: int, 
                           answer_type: str = "incorrect") -> Optional[int]:
        """Create a test response"""
        print(f"✍️ Creating test response for attempt {attempt_id}, question {question_id}...")
        
        answers = {
            "incorrect": "Python is not a programming language, it is a snake. Programming languages are tools for making websites.",
            "correct": "A programming language is a formal system of communication used to give instructions to computers. Examples include Python (for data science and web development), Java (for enterprise applications), and JavaScript (for web development).",
            "partial": "Programming languages are tools used to write code. Examples include Python and Java."
        }
        
        response_data = {
            "attempt_id": attempt_id,
            "question_id": question_id,
            "answer_text": answers.get(answer_type, answers["incorrect"]),
            "is_correct": answer_type == "correct"
        }
        
        try:
            response = requests.post(
                f"{self.config.backend_url}/api/v1/responses/",
                headers=self.config.headers,
                data=json.dumps(response_data)
            )
            
            if response.status_code == 201:
                response_id = response.json()["id"]
                self.created_resources["responses"].append(response_id)
                print(f"  ✅ Created response ID: {response_id} ({answer_type})")
                return response_id
            else:
                print(f"  ❌ Failed to create response: {response.text}")
                return None
                
        except Exception as e:
            print(f"  ❌ Error creating response: {e}")
            return None
    
    def complete_attempt(self, attempt_id: int, score: float = 0.0) -> bool:
        """Complete a quiz attempt"""
        print(f"🏁 Completing attempt {attempt_id}...")
        
        try:
            response = requests.post(
                f"{self.config.backend_url}/api/v1/attempts/{attempt_id}/complete",
                headers=self.config.headers,
                data=json.dumps({"score": score})
            )
            
            if response.status_code == 200:
                print(f"  ✅ Completed attempt with score: {score}%")
                return True
            else:
                print(f"  ❌ Failed to complete attempt: {response.text}")
                return False
                
        except Exception as e:
            print(f"  ❌ Error completing attempt: {e}")
            return False
    
    def request_ai_feedback(self, response_id: int) -> bool:
        """Request AI feedback generation for a response"""
        print(f"🤖 Requesting AI feedback for response {response_id}...")
        
        try:
            response = requests.post(
                f"{self.config.backend_url}/api/v1/feedback/request/{response_id}",
                headers=self.config.headers
            )
            
            if response.status_code == 202:
                print("  ✅ AI feedback generation requested")
                return True
            else:
                print(f"  ❌ Failed to request feedback: {response.text}")
                return False
                
        except Exception as e:
            print(f"  ❌ Error requesting feedback: {e}")
            return False
    
    def check_feedback_status(self, response_id: int, max_retries: int = 10) -> Optional[Dict[str, Any]]:
        """Check if AI feedback has been generated"""
        print(f"🔍 Checking feedback status for response {response_id}...")
        
        for attempt in range(max_retries):
            try:
                response = requests.get(
                    f"{self.config.backend_url}/api/v1/feedback/by_response/",
                    headers=self.config.headers,
                    params={"response_id": response_id}
                )
                
                if response.status_code == 200:
                    feedback_data = response.json()
                    if feedback_data:  # Not null
                        print("  ✅ Feedback found!")
                        print(f"  📊 Confidence: {feedback_data.get('confidence_score', 0):.2%}")
                        print(f"  🏷️ Error types: {feedback_data.get('error_type', [])}")
                        return feedback_data
                
                print(f"  ⏳ Attempt {attempt + 1}/{max_retries} - No feedback yet, waiting...")
                time.sleep(2)
                
            except Exception as e:
                print(f"  ❌ Error checking feedback: {e}")
                time.sleep(2)
        
        print(f"  ⚠️ No feedback found after {max_retries} attempts")
        return None
    
    def test_ai_service_direct(self, response_id: int = 28) -> bool:
        """Test AI service directly with sample data"""
        print("🔬 Testing AI service directly...")
        
        test_data = {
            "quiz_id": "2",
            "question_id": "7",
            "student_id": "7",
            "student_answer": "Python is not a programming language, it is a snake. Programming languages are tools for making websites.",
            "question_text": "Explain what a programming language is and give three examples.",
            "model_answer": "A programming language is a formal language comprising a set of instructions that can be used to produce various kinds of output. Examples include Python, Java, and JavaScript.",
            "key_concepts": ["programming language", "formal language", "instructions", "output", "examples"],
            "context_info": {
                "topic": "Introduction to Programming",
                "difficulty": "medium"
            }
        }
        
        try:
            response = requests.post(
                f"{self.config.ai_service_url}/ai-api/feedback/generate",
                headers={"Content-Type": "application/json"},
                data=json.dumps(test_data)
            )
            
            if response.status_code == 200:
                feedback = response.json()
                print(f"  ✅ AI service working!")
                print(f"  📝 Feedback: {feedback['feedback']['feedback_text'][:100]}...")
                print(f"  🎯 Confidence: {feedback['feedback']['confidence_score']:.2%}")
                return True
            else:
                print(f"  ❌ AI service error: {response.text}")
                return False
                
        except Exception as e:
            print(f"  ❌ Error testing AI service: {e}")
            return False
    
    def get_attempt_responses(self, attempt_id: int) -> Optional[Dict[str, Any]]:
        """Get detailed responses for an attempt"""
        print(f"📋 Getting responses for attempt {attempt_id}...")
        
        try:
            response = requests.get(
                f"{self.config.backend_url}/api/v1/responses/by_attempt/",
                headers=self.config.headers,
                params={"attempt_id": attempt_id}
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"  ✅ Found {len(data['responses'])} responses")
                print(f"  📊 Score: {data['attempt']['score']}%")
                return data
            else:
                print(f"  ❌ Failed to get responses: {response.text}")
                return None
                
        except Exception as e:
            print(f"  ❌ Error getting responses: {e}")
            return None
    
    def cleanup_test_data(self) -> None:
        """Clean up created test data"""
        print("🧹 Cleaning up test data...")
        
        # Note: In a real implementation, you'd want proper delete endpoints
        # For now, we just track what we created
        print(f"  📝 Created questions: {self.created_resources['questions']}")
        print(f"  🎯 Created attempts: {self.created_resources['attempts']}")
        print(f"  ✍️ Created responses: {self.created_resources['responses']}")
        print("  ℹ️  Manual cleanup may be required in database")
    
    def run_full_test_suite(self) -> bool:
        """Run the complete test suite"""
        print("🚀 Running full AI feedback test suite...\n")
        
        # 1. Health check
        if not self.test_health_check():
            print("❌ Services not healthy, aborting tests")
            return False
        
        print()
        
        # 2. Test AI service directly
        if not self.test_ai_service_direct():
            print("❌ AI service direct test failed")
            return False
        
        print()
        
        # 3. Create test data
        question_id = self.create_test_question()
        if not question_id:
            return False
        
        attempt_id = self.create_test_attempt()
        if not attempt_id:
            return False
        
        response_id = self.create_test_response(attempt_id, question_id, "incorrect")
        if not response_id:
            return False
        
        print()
        
        # 4. Complete attempt
        if not self.complete_attempt(attempt_id, 25.0):
            return False
        
        print()
        
        # 5. Request AI feedback
        if not self.request_ai_feedback(response_id):
            return False
        
        print()
        
        # 6. Check feedback status
        feedback = self.check_feedback_status(response_id)
        if not feedback:
            print("⚠️ Feedback generation may have failed")
        
        print()
        
        # 7. Get attempt responses
        responses_data = self.get_attempt_responses(attempt_id)
        if responses_data:
            print("✅ Full test suite completed successfully!")
            print("\n📋 Test Results Summary:")
            print(f"  Question ID: {question_id}")
            print(f"  Attempt ID: {attempt_id}")
            print(f"  Response ID: {response_id}")
            print(f"  Feedback Generated: {'Yes' if feedback else 'No'}")
            print(f"\n🌐 View results at: http://localhost:5173/attempts/{attempt_id}")
        
        return True


def main():
    parser = argparse.ArgumentParser(description="AI Feedback System Test Script")
    parser.add_argument("--test-all", action="store_true", help="Run full test suite")
    parser.add_argument("--create-test-data", action="store_true", help="Create test data only")
    parser.add_argument("--test-feedback", action="store_true", help="Test feedback generation")
    parser.add_argument("--response-id", type=int, help="Response ID for feedback testing")
    parser.add_argument("--cleanup", action="store_true", help="Show cleanup information")
    parser.add_argument("--health-check", action="store_true", help="Check service health")
    parser.add_argument("--ai-direct", action="store_true", help="Test AI service directly")
    
    args = parser.parse_args()
    
    config = TestConfig()
    tester = AIFeedbackTester(config)
    
    if args.health_check:
        tester.test_health_check()
    
    elif args.ai_direct:
        tester.test_ai_service_direct()
    
    elif args.test_all:
        tester.run_full_test_suite()
    
    elif args.create_test_data:
        question_id = tester.create_test_question()
        if question_id:
            attempt_id = tester.create_test_attempt()
            if attempt_id:
                response_id = tester.create_test_response(attempt_id, question_id, "incorrect")
                print(f"\n✅ Test data created - Question: {question_id}, Attempt: {attempt_id}, Response: {response_id}")
    
    elif args.test_feedback:
        if args.response_id:
            tester.request_ai_feedback(args.response_id)
            tester.check_feedback_status(args.response_id)
        else:
            print("❌ --response-id required for feedback testing")
    
    elif args.cleanup:
        tester.cleanup_test_data()
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main() 