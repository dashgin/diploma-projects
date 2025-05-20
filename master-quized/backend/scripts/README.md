# Database Seed Scripts

This directory contains scripts to populate the database with sample data for development and testing.

## seed_data.py

This script populates the database with sample data for the QuizEd application, including:

- Users (educators and students)
- Knowledge areas (Mathematics, Science, Programming, etc.)
- Quizzes with multiple-choice and short-answer questions
- Study classes
- Student enrollments in classes
- Quiz assignments
- Student attempts and responses

### Prerequisites

Before running the script, make sure:

1. The database is set up and migrations have been applied
2. The application environment is properly configured

The script now automatically creates test users if they don't exist:
- Educator: educator@example.com (password: educator123)
- Students: student1@example.com through student5@example.com (passwords: student1, student2, etc.)

### Running the script

From the project root directory:

```bash
# Navigate to the backend directory
cd backend

# Activate the virtual environment (if not already activated)
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
# .venv\Scripts\activate

# Run the script
python scripts/seed_data.py
```

Or using the executable directly:

```bash
# Navigate to the backend directory
cd backend

# Activate the virtual environment (if not already activated)
source .venv/bin/activate

# Run the script
./scripts/seed_data.py
```

### Sample Data Created

The script creates:

1. **Users**:
   - 1 educator
   - 5 students

2. **Knowledge Areas**:
   - Mathematics
   - Science
   - Programming
   - History
   - Languages

3. **Quizzes**:
   - Basic Mathematics Quiz
   - Introduction to Programming

4. **Questions**:
   - Multiple-choice questions with options
   - Short-answer questions with model answers

5. **Study Classes**:
   - Mathematics 101
   - Programming Fundamentals

6. **Assignments, Attempts, and Responses**:
   - Quiz assignments to students
   - Student attempts (some completed, some in progress)
   - Student responses (correct and incorrect)

### Extending the Script

To add more sample data:

1. Add new quiz questions to the `math_questions` or `programming_questions` lists
2. Create additional quizzes by following the pattern in the `main()` function
3. Add more knowledge areas to the `create_knowledge_areas()` function
4. Modify the user creation in the `main()` function to add different types of users 