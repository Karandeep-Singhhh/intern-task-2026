# Language Feedback API

## Overview
Built an **LLM-powered language feedback API** that analyzes learner-written sentences and returns structured correction feedback.

## Design Decisions
- Decided to use Claude out of personal preference and access to ClaudeCode/pro models through my school providing a free subscription.
  - This meant changing all basic boilerplate code that referenced the preset OpenAI API key to using my Claude key.
- Chose claude-sonnet-4-6 — can be scaled and isn't as costly as other models like Opus-4-6
- Single-call prompt approach — reliable, fast, within 30s limit
- Temperature set to 0.2 for consistent output

## Prompt Strategy

### Preemptive Design Decisions
- Instructed model to return raw JSON only (no markdown wrapping). That being said, LLMs are only so reliable as we programmers are aware, so I have implemented a response checker as a safety net to ensure it is usable JSON only.
- Emphasized correct sentence handling explicitly to prevent hallucinated errors — you are not an error finder, you are a sentence analyzer.
- Added preemptive emphasis on multi-word phrasal grammar to improve detection of errors like missing prepositions.
- Added preemptive rules to prevent certain errors.

### Post-Testing Adjustments
- Testing the Japanese sample highlighted a weakness: direct translations vs conversational understanding. The model responded in a description with "the place where you are settled" to refer to where someone lives. This is too formal, and the word "settled" is an awkward phrasing that wouldn't be used in conversation. Thus, I changed the final rule to emphasize that explanations should make sense in conversation, and that word choice and translations should sound like a native speaker. This change resulted in new phrasing of "not places you reside," which is much clearer.
- Testing the Portuguese sample showed a shortcoming, the model missed an error and thus misclassified the difficulty level as well. The error was due to a required grammatical choice. Initial thoughts: the word that required the preemptive word was about 4 words away. I presume the model isn't emphasizing the importance of longer phrases as such being grammatically correct, which may also be partly due to the fact that it is Portuguese rather than English. Adding adjustments accordingly was not sufficient. I identify this as a prepositional error, which the model evidently misses repeatedly. I expect iteration of some sort would fix this, however.

## Known Limitations
- Subtle prepositional errors in Portuguese (and likely other languages) are occasionally missed.
- Non-ASCII input via terminal has encoding issues on Windows — use file-based input (`-d @file.json`) as workaround. Testing the Japanese sample showed that certain scripts have parsing issues in which the model is unable to read or understand the input at all. To work around this, the input was written in a separate json file, which was called in the POST request. This works because through Git Bash Terminals on Windows, the shell's input handling has known issues with encoding non-ASCII characters, however, in a separate file curl reads the information directly from the file rather than through the shell.

## How to Run

### Local
```bash
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
cp .env.example .env  # add ANTHROPIC_API_KEY
uvicorn app.main:app --reload
```

### Docker
```bash
cp .env.example .env
docker compose up --build
```

### Tests
```bash
pytest tests/test_feedback_unit.py tests/test_schema.py -v
pytest tests/test_feedback_integration.py -v  # requires API key
```
