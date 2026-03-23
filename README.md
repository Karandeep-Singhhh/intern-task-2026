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
<<<<<<< HEAD

## How to Submit

1. **Fork** this repository
2. Replace the sample implementation with your own
3. Make sure `docker compose up` works and passes the health check
4. Push to your fork
5. **Fill out the [submission form](https://forms.gle/ukcypgRiMgGhvnBh8)** with your name, email, and the link to your fork

**Use the same email you applied with on Handshake.** This is how we match your submission to your application.

**Deadline: Sunday, March 22, 2026 at 11:59 PM Eastern Time.** Late submissions will not be evaluated.

## How Submissions Are Evaluated

| Criterion                  | Weight | Method      | Description                                                                                    |
| -------------------------- | ------ | ----------- | ---------------------------------------------------------------------------------------------- |
| **Runs successfully**      | Gate   | Automated   | Server starts via Docker and responds to health check. **Fail = disqualified.**                |
| **Schema compliance**      | Gate   | Automated   | ≥90% of responses match JSON schema. **Below threshold = disqualified.**                       |
| **Response time**          | Gate   | Automated   | Each `/feedback` request must return within 30 seconds. **Timeouts = failures.**               |
| **Accuracy**               | 25%    | Absolute    | Corrections are linguistically accurate across a hidden test suite spanning multiple languages |
| **Production feasibility** | 25%    | Comparative | Could this run at scale? Model choice, token efficiency, caching, cost reduction strategy      |
| **Test quality**           | 25%    | Comparative | Your tests are meaningful, cover edge cases, and test real behavior                            |
| **Code & prompt quality**  | 25%    | Comparative | Clean code, thoughtful prompt design, clear README                                             |

> **How comparative scoring works:** Accuracy is scored on an absolute scale: your API is tested against a hidden test suite and judged on correctness. The three subjective dimensions (production feasibility, test quality, code & prompt quality) are evaluated through **direct head-to-head comparison** between submissions. This means your rating in these dimensions reflects how your approach compares to other applicants, not an arbitrary absolute threshold. We use this approach because LLMs are more reliable at saying "A is better than B" than at assigning consistent absolute scores. (Think of how judges at competitions compare entries side by side.)

## What We're Looking For

- **Prompt engineering skill.** Can you get an LLM to reliably produce structured, accurate output?
- **Software craft.** Clean code, proper error handling, good test coverage.
- **Product thinking.** Do your design decisions reflect someone who thinks about the end user (a language learner)?
- **Cost-effectiveness.** Could this run in production without burning money? Model choice, token usage, and caching strategy matter.
- **Communication.** Can you explain your approach clearly in writing?

## When Is My Submission "Done"?

Your submission is ready when:

1. **It works**: `docker compose up` starts cleanly, the health check passes, and `/feedback` returns valid JSON for a variety of inputs (different languages, correct sentences, sentences with errors, non-Latin scripts).
2. **It's tested**: You have a meaningful test suite that you'd be comfortable showing to a colleague.
3. **It's explained**: Your README describes what you built, why you made the choices you did, and how to run it.
4. **You'd ship it**: If someone said "we're deploying this tomorrow," you wouldn't be embarrassed.

Don't chase perfection. A clean, working submission that does the basics well will outperform an ambitious half-finished one. Depth in one area (a great prompt, a thorough test suite, a clever optimization) can set you apart, but only if the foundations are solid first.

Your submission must use **Python** and either **OpenAI** or **Anthropic** as your LLM provider. You are free to use any Python web framework (FastAPI, Flask, Django, etc.) and any OpenAI or Anthropic model. The sample submission uses Python + FastAPI + OpenAI.

> **Important**: The automated scorer runs your tests _inside_ your Docker container via `docker compose exec feedback-api`. Make sure your test dependencies are installed in your Docker image and that your Docker Compose service is named `feedback-api`.

## Example I/O

See [examples/sample_inputs.json](examples/sample_inputs.json) for 5 example input/output pairs covering Spanish, French, Japanese, German, and Portuguese.

## FAQ

**What LLM can I use?**
OpenAI or Anthropic. You can use any model from either provider, and you can chain or combine models from both. Your choice of model is part of your design, so own it and explain it in your README.

**Do I have to use Python / FastAPI / OpenAI?**
Python is required. FastAPI is not: you can use Flask, Django, or any other Python web framework. For LLM providers, you must use OpenAI, Anthropic, or both.

**Do I need to pay for an API key?**
OpenAI and Anthropic both offer free trial credits for new accounts, which should be more than enough for this task.

**Can I use AI tools like ChatGPT or Copilot?**
Yes, fully allowed. See the [AI Use section in RULES.md](RULES.md#ai-use) for our take on this.

**What if my API returns slightly different output than the examples?**
That's fine. The examples show the shape we expect. Exact wording of explanations, corrections, etc. will naturally vary. Your response must conform to the JSON schema, but the linguistic content is judged on accuracy, not exact string matching.

**What if the input sentence is already correct?**
Return `is_correct: true`, an empty `errors` array, and set `corrected_sentence` to the original sentence. This is tested.

**How many languages do I need to support?**
Your API should handle any language a user might submit. The hidden test suite covers 8+ languages including non-Latin scripts (Japanese, Korean, Russian, Chinese). You don't need language-specific logic (the LLM handles this), but your prompt should be robust enough to work across scripts and writing systems.

**Do I need to speak the languages being tested?**
No. The whole point is that the LLM does the linguistic heavy lifting. But you should think about how to verify accuracy for languages you don't know (hint: that's a good thing to discuss in your README).

**Can I modify the JSON schemas?**
No. Your response must conform to the provided `schema/response.schema.json`. You can add extra fields, but the required fields and their types must match.

**What does "replace this README" mean?**
When you submit, your fork's README should describe _your_ approach: your design decisions, prompt strategy, how to run it, and anything interesting you tried. Delete the task description and write your own.

**What if Docker isn't working on my machine?**
Your server must be runnable via `docker compose up`. If you're having Docker issues locally, make sure your Dockerfile works. We will run it in a clean environment. If you need help, that's a fine thing to Google or ask an AI about.

**Is housing provided for the internship?**
No. The internship is on-site in Richmond, Virginia. You are responsible for your own housing and transportation. Richmond has a relatively low cost of living compared to major tech hubs. Summer sublets near VCU and the Fan District are typically $600–900/month.

**I'm an international student with a valid work permit (e.g., CPT/OPT). Am I eligible?**
Yes, as long as you are authorized to work in the United States during the internship period (June–August 2026). We do not sponsor employment visas, but existing work authorization (CPT, OPT, etc.) is fine.

**Will I get feedback on my submission if I'm not selected?**
We can't provide individual feedback to all applicants given the volume, but we may publish general observations about what strong submissions had in common.

**Can I start over after forking?**
Yes. You can `git push --force` as many times as you like before the deadline. We only evaluate what's in your fork at the time the deadline passes.

**Who reviews the submissions?**
Initial scoring is fully automated (Docker build, schema validation, accuracy testing). Accuracy is scored by an LLM judge that runs **twice per submission** and averages the scores to reduce variance. Subjective dimensions (production feasibility, test quality, code quality) are scored through head-to-head comparison between submissions, so your rating reflects how your approach stacks up against the pool. The top submissions are reviewed in full by humans on the Pangea Chat team.

**I'm uncomfortable with automated scoring.**
We understand. We chose transparency over black-box screening: you can see exactly what's evaluated and how. The automated pipeline produces a shortlist; it does not make the hiring decision. Every top submission is reviewed in full by humans on our team.

## Questions?

If something is ambiguous, make a reasonable assumption, state it in your README, and move forward. This is part of the evaluation. We want to see how you handle ambiguity.

---

See [RULES.md](RULES.md) for full assessment rules, eligibility, and legal terms.
=======
>>>>>>> f93752f (final submission of task)
