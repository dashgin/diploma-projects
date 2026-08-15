# Assignment Components

This directory contains components for managing quiz assignments.

## Components

### AssignmentsList

Displays a list of assignments. Can show either all assignments or only the current user's assignments.

- Uses Chakra UI v3 Table components with proper styling
- Handles empty states appropriately
- Shows assignment status with colored badges

### AssignmentDetails

Shows detailed information about a specific assignment.

- Fetches related data (quiz, student, questions)
- Displays a visual representation of assignment status
- Provides a way to start the quiz

### CreateAssignment

Allows assigning a quiz to a student.

- Filter users by role "student"
- Setting due dates
- Integrated within quiz details page

## Integration Points

- The `QuizActions` component combines `EditQuiz` and `CreateAssignment` for use in the quiz details page
- Assignment routes provide navigation through the app

## Usage

```tsx
// List all assignments
<AssignmentsList />

// List user assignments
<AssignmentsList userAssignments={true} />

// Show assignment details
<AssignmentDetails assignmentId={123} />

// Create new assignment for a quiz
<CreateAssignment quizId={456} />
``` 