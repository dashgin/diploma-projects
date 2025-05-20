Here are the SQL schemas with improved table names that better reflect their purpose and entity relationships:

# SQL Schemas for QuizEd Database (Improved Naming)

## Users and Authentication

```sql
-- User table
CREATE TABLE auth_user (
    id SERIAL PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login TIMESTAMP NULL,
    is_superuser BOOLEAN NOT NULL DEFAULT FALSE,
    is_staff BOOLEAN NOT NULL DEFAULT FALSE,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    date_joined TIMESTAMP NOT NULL,
    name VARCHAR(255) NULL,
    email VARCHAR(254) NOT NULL UNIQUE,
    role VARCHAR(10) NOT NULL DEFAULT 'student'
);

-- User permissions join table
CREATE TABLE auth_user_groups (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    group_id INTEGER NOT NULL
);

-- User groups join table
CREATE TABLE auth_user_permissions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    permission_id INTEGER NOT NULL
);

-- Classes (Groups of students)
CREATE TABLE study_class (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    educator_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Class-Student many-to-many relationship
CREATE TABLE study_class_enrollment (
    id SERIAL PRIMARY KEY,
    class_id INTEGER NOT NULL REFERENCES study_class(id) ON DELETE CASCADE,
    student_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE
);
```

## Quiz Management

```sql
-- Knowledge Areas
CREATE TABLE knowledge_area (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Quizzes
CREATE TABLE quiz (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    instructions TEXT NULL,
    creator_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    area_id INTEGER NULL REFERENCES knowledge_area(id) ON DELETE SET NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

-- Questions
CREATE TABLE quiz_question (
    id SERIAL PRIMARY KEY,
    quiz_id INTEGER NOT NULL REFERENCES quiz(id) ON DELETE CASCADE,
    area_id INTEGER NULL REFERENCES knowledge_area(id) ON DELETE SET NULL,
    text TEXT NOT NULL,
    question_type VARCHAR(15) NOT NULL,
    order_position INTEGER NOT NULL DEFAULT 0,
    correct_answer TEXT NULL DEFAULT '',
    model_answer TEXT NULL DEFAULT '',
    key_concepts JSONB NULL,
    ai_guidance JSONB NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Multiple-choice Options
CREATE TABLE question_option (
    id SERIAL PRIMARY KEY,
    question_id INTEGER NOT NULL REFERENCES quiz_question(id) ON DELETE CASCADE,
    text VARCHAR(200) NOT NULL,
    is_correct BOOLEAN NOT NULL DEFAULT FALSE,
    order_position INTEGER NOT NULL DEFAULT 0
);
```

## Quiz Assignments and Attempts

```sql
-- Quiz Assignments
CREATE TABLE quiz_assignment (
    id SERIAL PRIMARY KEY,
    quiz_id INTEGER NOT NULL REFERENCES quiz(id) ON DELETE CASCADE,
    student_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    class_id INTEGER NULL REFERENCES study_class(id) ON DELETE CASCADE,
    assigned_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    due_date TIMESTAMP NULL
);

-- Quiz Attempts
CREATE TABLE student_attempt (
    id SERIAL PRIMARY KEY,
    assignment_id INTEGER NULL REFERENCES quiz_assignment(id) ON DELETE CASCADE,
    student_id INTEGER NOT NULL REFERENCES auth_user(id) ON DELETE CASCADE,
    quiz_id INTEGER NOT NULL REFERENCES quiz(id) ON DELETE CASCADE,
    started_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP NULL,
    score FLOAT NULL,
    is_completed BOOLEAN NOT NULL DEFAULT FALSE
);

-- Student Responses
CREATE TABLE student_response (
    id SERIAL PRIMARY KEY,
    attempt_id INTEGER NOT NULL REFERENCES student_attempt(id) ON DELETE CASCADE,
    question_id INTEGER NOT NULL REFERENCES quiz_question(id) ON DELETE CASCADE,
    answer_text TEXT NOT NULL,
    is_correct BOOLEAN NULL,
    selected_option_id INTEGER NULL REFERENCES question_option(id) ON DELETE SET NULL,
    submitted_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

## Feedback and Recommendations

```sql
-- AI-Generated Feedback
CREATE TABLE ai_feedback (
    id SERIAL PRIMARY KEY,
    response_id INTEGER NOT NULL UNIQUE REFERENCES student_response(id) ON DELETE CASCADE,
    feedback_text TEXT NOT NULL,
    feedback_content JSONB NOT NULL,
    generated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    error_type VARCHAR(50) NULL DEFAULT '',
    confidence_score FLOAT NULL,
    ai_metadata JSONB NULL
);

-- Resource Recommendations
CREATE TABLE learning_resource (
    id SERIAL PRIMARY KEY,
    feedback_id INTEGER NOT NULL REFERENCES ai_feedback(id) ON DELETE CASCADE,
    title VARCHAR(200) NOT NULL,
    description TEXT NULL,
    url VARCHAR(200) NULL,
    resource_type VARCHAR(50) NOT NULL,
    area_id INTEGER NULL REFERENCES knowledge_area(id) ON DELETE SET NULL,
    relevance_score FLOAT NULL
);
```

## Indexes

```sql
-- User table indexes
CREATE INDEX idx_user_email ON auth_user(email);
CREATE INDEX idx_user_role ON auth_user(role);

-- Class table indexes
CREATE INDEX idx_class_educator ON study_class(educator_id);

-- Quiz table indexes
CREATE INDEX idx_quiz_creator ON quiz(creator_id);
CREATE INDEX idx_quiz_area ON quiz(area_id);
CREATE INDEX idx_quiz_active ON quiz(is_active);

-- Question table indexes
CREATE INDEX idx_question_quiz ON quiz_question(quiz_id);
CREATE INDEX idx_question_area ON quiz_question(area_id);
CREATE INDEX idx_question_type ON quiz_question(question_type);

-- Option table indexes
CREATE INDEX idx_option_question ON question_option(question_id);

-- Assignment table indexes
CREATE INDEX idx_assignment_quiz ON quiz_assignment(quiz_id);
CREATE INDEX idx_assignment_student ON quiz_assignment(student_id);

-- Attempt table indexes
CREATE INDEX idx_attempt_student ON student_attempt(student_id);
CREATE INDEX idx_attempt_quiz ON student_attempt(quiz_id);
CREATE INDEX idx_attempt_assignment ON student_attempt(assignment_id);
CREATE INDEX idx_attempt_completed ON student_attempt(is_completed);

-- Response table indexes
CREATE INDEX idx_response_attempt ON student_response(attempt_id);
CREATE INDEX idx_response_question ON student_response(question_id);

-- Feedback table indexes
CREATE INDEX idx_feedback_response ON ai_feedback(response_id);

-- Recommendation table indexes
CREATE INDEX idx_resource_feedback ON learning_resource(feedback_id);
CREATE INDEX idx_resource_area ON learning_resource(area_id);
CREATE INDEX idx_resource_type ON learning_resource(resource_type);
```
