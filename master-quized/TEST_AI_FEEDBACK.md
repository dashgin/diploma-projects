# AI Feedback System Test Script

This comprehensive test script validates the complete AI feedback pipeline for the QuizEd application, covering all the API endpoints and functionality implemented during development.

## Features

- 🔍 **Health Checks**: Verify backend and AI service availability
- 📝 **Test Data Creation**: Generate questions, attempts, and responses
- 🤖 **AI Feedback Testing**: Request and validate feedback generation
- 📊 **End-to-End Validation**: Complete workflow testing
- 🧹 **Resource Tracking**: Track created test data for cleanup

## Prerequisites

1. **Services Running**:
   - Backend: `http://localhost:8000`
   - AI Service: `http://localhost:8001`
   - Frontend: `http://localhost:5173` (optional, for viewing results)

2. **Authentication Token**: Update the `access_token` in the script with a valid JWT token

3. **Python Dependencies**:
   ```bash
   pip install -r test_requirements.txt
   ```

## Usage Examples

### 🚀 Run Full Test Suite
```bash
python test_ai_feedback.py --test-all
```
This runs the complete end-to-end test including:
- Health checks for all services
- Direct AI service testing
- Creating test question, attempt, and response
- Completing the attempt
- Requesting AI feedback generation
- Verifying feedback was created
- Displaying results summary

### 🔍 Health Check Only
```bash
python test_ai_feedback.py --health-check
```
Quickly verify that backend and AI service are running.

### 🔬 Test AI Service Directly
```bash
python test_ai_feedback.py --ai-direct
```
Send a request directly to the AI service to verify it's generating feedback correctly.

### 📝 Create Test Data Only
```bash
python test_ai_feedback.py --create-test-data
```
Create a new question, attempt, and response for manual testing.

### 🤖 Test Feedback for Existing Response
```bash
python test_ai_feedback.py --test-feedback --response-id 28
```
Request AI feedback for an existing response ID and check the results.

### 🧹 Cleanup Information
```bash
python test_ai_feedback.py --cleanup
```
Display information about created test resources (manual cleanup required).

## Test Scenarios

The script includes multiple test scenarios:

### 1. Incorrect Answer Test
- **Student Answer**: "Python is not a programming language, it is a snake. Programming languages are tools for making websites."
- **Expected AI Feedback**: Error identification, concept analysis, resource recommendations

### 2. Correct Answer Test
- **Student Answer**: "A programming language is a formal system of communication used to give instructions to computers. Examples include Python, Java, and JavaScript."
- **Expected AI Feedback**: Positive feedback, concept validation

### 3. Partial Answer Test
- **Student Answer**: "Programming languages are tools used to write code. Examples include Python and Java."
- **Expected AI Feedback**: Mixed feedback with improvement suggestions

## API Endpoints Tested

### Backend Endpoints
- `GET /api/v1/utils/health-check` - Service health
- `POST /api/v1/questions/` - Create question
- `POST /api/v1/attempts/` - Create attempt
- `POST /api/v1/responses/` - Create response
- `POST /api/v1/attempts/{id}/complete` - Complete attempt
- `POST /api/v1/feedback/request/{response_id}` - Request AI feedback
- `GET /api/v1/feedback/by_response/` - Get feedback by response
- `GET /api/v1/responses/by_attempt/` - Get attempt responses

### AI Service Endpoints
- `GET /health` - AI service health
- `POST /feedback/generate` - Generate feedback directly

## Example Output

```
🚀 Running full AI feedback test suite...

🔍 Testing service health...
  Backend: ✅ Healthy
  AI Service: ✅ Healthy

🔬 Testing AI service directly...
  ✅ AI service working!
  📝 Feedback: Your answer addresses some important aspects but could be improved...
  🎯 Confidence: 20%

📝 Creating test question for quiz 2...
  ✅ Created question ID: 8

🎯 Creating test attempt for quiz 2...
  ✅ Created attempt ID: 9

✍️ Creating test response for attempt 9, question 8...
  ✅ Created response ID: 29 (incorrect)

🏁 Completing attempt 9...
  ✅ Completed attempt with score: 25.0%

🤖 Requesting AI feedback for response 29...
  ✅ AI feedback generation requested

🔍 Checking feedback status for response 29...
  ✅ Feedback found!
  📊 Confidence: 20%
  🏷️ Error types: ['irrelevant_content']

📋 Getting responses for attempt 9...
  ✅ Found 1 responses
  📊 Score: 25.0%

✅ Full test suite completed successfully!

📋 Test Results Summary:
  Question ID: 8
  Attempt ID: 9
  Response ID: 29
  Feedback Generated: Yes

🌐 View results at: http://localhost:5173/attempts/9
```

## Configuration

Update the `TestConfig` class to match your environment:

```python
@dataclass
class TestConfig:
    backend_url: str = "http://localhost:8000"
    ai_service_url: str = "http://localhost:8001"
    access_token: str = "your-jwt-token-here"
```

## Troubleshooting

### Services Not Responding
```bash
# Check if services are running
curl http://localhost:8000/api/v1/utils/health-check
curl http://localhost:8001/health
```

### Authentication Issues
- Ensure your JWT token is valid and not expired
- Token should have appropriate permissions for creating resources

### Feedback Generation Failing
- Check AI service logs for errors
- Verify the response has text content (not just multiple choice)
- Ensure the question has proper `key_concepts` and `model_answer`

### No Feedback After Request
- AI feedback generation runs in background (can take 5-10 seconds)
- Check backend logs for any errors in the background task
- Verify AI service is reachable from backend container/process

## Integration with Development Workflow

This script is perfect for:
- **Automated Testing**: Include in CI/CD pipeline
- **Development Validation**: Quick verification during development
- **Demo Preparation**: Create consistent test data for demonstrations
- **Debugging**: Isolate and test specific components
- **Performance Testing**: Measure feedback generation times

## Contributing

When adding new AI feedback features:
1. Add corresponding test methods to the `AIFeedbackTester` class
2. Update the test scenarios with new edge cases
3. Document expected behavior in this README
4. Ensure cleanup procedures handle new resource types 