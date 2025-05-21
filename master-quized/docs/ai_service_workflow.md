# AI Service Workflow

## Request Flow

1. Client sends a `FeedbackRequest` to `/feedback/generate` endpoint containing:
   - `quiz_id` and `question_id`: Identifiers
   - `student_id`: Student identifier
   - `student_answer`: The response to evaluate
   - `question_text`: The original question
   - `model_answer`: The reference answer
   - `key_concepts`: List of expected concepts
   - `context_info`: Additional context (optional)

2. FastAPI server receives the request and begins processing

## Processing Pipeline

### Stage 1: Preprocessing
- Both student answer and model answer are normalized using `preprocessing.preprocess_text()`
- This includes text normalization, stemming, and removal of stopwords

### Stage 2: Rule-Based Analysis
- The `rule_based_feedback.apply_rules()` function evaluates against predefined rules
- If immediate feedback is warranted (e.g., missing key terms, blank answer), an early response is generated

### Stage 3: ML/NLP Analysis (if rule-based checks passed)
- `ml_analysis.analyze_response()` performs deep semantic analysis:
  1. Semantic similarity calculation (student vs. model answer)
  2. Error classification to identify misconceptions
  3. Concept identification to determine which concepts were addressed

### Stage 4: Skill Gap Identification
- `ml_analysis.identify_skill_gaps()` determines which key concepts the student missed

### Stage 5: Resource Recommendation
- `recommendation_engine.get_recommendations()` suggests learning resources based on identified gaps

### Stage 6: Feedback Construction
- `feedback_generation.construct_feedback()` combines all analysis results into a coherent feedback message

## Response Flow

The server returns a `FeedbackResponse` containing:
- `status`: Success indicator
- `message`: Status message
- `feedback`: A `FeedbackResponseData` object with:
  - `feedback_text`: Personalized feedback 
  - `error_identified`: Whether errors were found
  - `error_type`: List of error types (if any)
  - `confidence_score`: AI confidence in the analysis
  - `concepts_covered`: Concepts addressed by the student
  - `concepts_missed`: Concepts the student missed
  - `recommended_resources`: List of learning resources (each as a `RecommendedResource`)

## Models Used

1. **Semantic Similarity Model**: Sentence transformer (`all-MiniLM-L6-v2` by default)
2. **Error Classifier Model**: DistilBERT-based classifier (custom or fallback to `distilbert-base-uncased`)

## Performance Optimizations

- `@lru_cache` decorators on compute-intensive functions
- Lazy loading of ML models using global variables
- Graceful degradation when models fail to load 