QuizEd API Endpoints
User Endpoints
GET /api/v1/users/{id}/ - Retrieve a specific user
GET /api/v1/users/me/ - Get the currently logged-in user's profile
Quiz Management Endpoints
Areas
GET /api/v1/areas/ - List all knowledge areas
Quizzes
GET /api/v1/quizzes/ - List all quizzes (filtered by user role)
POST /api/v1/quizzes/ - Create a new quiz
GET /api/v1/quizzes/{id}/ - Retrieve a specific quiz
PUT /api/v1/quizzes/{id}/ - Update a quiz
PATCH /api/v1/quizzes/{id}/ - Partially update a quiz
DELETE /api/v1/quizzes/{id}/ - Delete a quiz
GET /api/v1/quizzes/my_quizzes/ - Get quizzes created by the current user (educators only)
Questions
GET /api/v1/questions/ - List all questions (not recommended)
POST /api/v1/questions/ - Create a new question
GET /api/v1/questions/{id}/ - Retrieve a specific question
PUT /api/v1/questions/{id}/ - Update a question
PATCH /api/v1/questions/{id}/ - Partially update a question
DELETE /api/v1/questions/{id}/ - Delete a question
GET /api/v1/questions/by_quiz/ - Get questions for a specific quiz (requires quiz_id parameter)
Options (Multiple-choice items)
POST /api/v1/items/ - Create a new option
GET /api/v1/items/{id}/ - Retrieve a specific option
PUT /api/v1/items/{id}/ - Update an option
PATCH /api/v1/items/{id}/ - Partially update an option
DELETE /api/v1/items/{id}/ - Delete an option
GET /api/v1/items/by_question/ - Get options for a specific question (requires question_id parameter)
Assignment and Attempt Endpoints
Quiz Assignments
GET /api/v1/assignments/ - List quiz assignments
POST /api/v1/assignments/ - Create a new quiz assignment
GET /api/v1/assignments/{id}/ - Retrieve a specific quiz assignment
GET /api/v1/assignments/my_assignments/ - Get assignments for the current user
Quiz Attempts
GET /api/v1/attempts/ - List quiz attempts
POST /api/v1/attempts/ - Create a new quiz attempt
GET /api/v1/attempts/{id}/ - Retrieve a specific quiz attempt
POST /api/v1/attempts/{id}/complete/ - Mark a quiz attempt as completed
GET /api/v1/attempts/my_attempts/ - Get attempts for the current user
Responses
POST /api/v1/responses/ - Create a new response
GET /api/v1/responses/{id}/ - Retrieve a specific response
GET /api/v1/responses/by_attempt/ - Get responses for a specific quiz attempt (requires attempt_id parameter)
Feedback and Recommendation Endpoints
Feedback
POST /api/v1/feedback/ - Create new feedback
GET /api/v1/feedback/{id}/ - Retrieve specific feedback
GET /api/v1/feedback/by_response/ - Get feedback for a specific response (requires response_id parameter)
Resource Recommendations
POST /api/v1/recommendations/ - Create a new resource recommendation
GET /api/v1/recommendations/{id}/ - Retrieve a specific resource recommendation
GET /api/v1/recommendations/by_feedback/ - Get recommendations for a specific feedback (requires feedback_id parameter)
All endpoints require authentication with JWT tokens, and data access is restricted based on user roles (educator or student).