"""Integration tests -- require ANTHROPIC_API_KEY to be set.

Run with: pytest tests/test_feedback_integration.py -v

These tests make real API calls. Skip them in CI or when no key is available.
"""

import os

import pytest
from app.feedback import get_feedback
from app.models import FeedbackRequest

pytestmark = pytest.mark.skipif(
    not os.getenv("ANTHROPIC_API_KEY"),
    reason="ANTHROPIC_API_KEY not set -- skipping integration tests",
)

VALID_ERROR_TYPES = {
    "grammar",
    "spelling",
    "word_choice",
    "punctuation",
    "word_order",
    "missing_word",
    "extra_word",
    "conjugation",
    "gender_agreement",
    "number_agreement",
    "tone_register",
    "other",
}
VALID_DIFFICULTIES = {"A1", "A2", "B1", "B2", "C1", "C2"}


@pytest.mark.asyncio
async def test_spanish_error():
    result = await get_feedback(
        FeedbackRequest(
            sentence="Yo soy fue al mercado ayer.",
            target_language="Spanish",
            native_language="English",
        )
    )
    assert result.is_correct is False
    assert len(result.errors) >= 1
    assert result.difficulty in VALID_DIFFICULTIES
    for error in result.errors:
        assert error.error_type in VALID_ERROR_TYPES
        assert len(error.explanation) > 0


@pytest.mark.asyncio
async def test_correct_german():
    result = await get_feedback(
        FeedbackRequest(
            sentence="Ich habe gestern einen interessanten Film gesehen.",
            target_language="German",
            native_language="English",
        )
    )
    assert result.is_correct is True
    assert result.errors == []
    assert result.difficulty in VALID_DIFFICULTIES


@pytest.mark.asyncio
async def test_french_gender_errors():
    result = await get_feedback(
        FeedbackRequest(
            sentence="La chat noir est sur le table.",
            target_language="French",
            native_language="English",
        )
    )
    assert result.is_correct is False
    assert len(result.errors) >= 1


@pytest.mark.asyncio
async def test_japanese_particle():
    result = await get_feedback(
        FeedbackRequest(
            sentence="私は東京を住んでいます。",
            target_language="Japanese",
            native_language="English",
        )
    )
    assert result.is_correct is False
    assert any("に" in e.correction for e in result.errors)


# Added tests

# Testing correct sentence in non-Latin script - model should not make up errors
@pytest.mark.asyncio
async def test_correct_arabic():
    result = await get_feedback(
        FeedbackRequest(
            sentence="أنا ذاهب إلى المتجر لأشتري بعض الحليب.",
            target_language="Arabic",
            native_language="English",
        )
    )
    assert result.is_correct is True
    assert result.errors == []


# Testing multiple different error types in one sentence
@pytest.mark.asyncio
async def test_multiple_error_types():
    result = await get_feedback(
        FeedbackRequest(
            sentence="She go to store yesterday and buyed some apple.",
            target_language="English",
            native_language="Spanish",
        )
    )
    assert result.is_correct is False
    assert len(result.errors) >= 2
    error_types = {e.error_type for e in result.errors}
    assert len(error_types) >= 2
    for error in result.errors:
        assert error.error_type in VALID_ERROR_TYPES


# Testing explanations are returned in the learner's native language
@pytest.mark.asyncio
async def test_explanation_in_native_language():
    result = await get_feedback(
        FeedbackRequest(
            sentence="I go to the store yesterday.",
            target_language="English",
            native_language="French",
        )
    )
    assert result.is_correct is False
    assert len(result.errors) >= 1
    # Explanation should contain French, not solely English
    combined = " ".join(e.explanation for e in result.errors).lower()
    french_indicators = ["le", "la", "les", "est", "vous", "tu", "verbe", "temps", "passé", "hier"]
    assert any(word in combined for word in french_indicators)


# Testing word order error
@pytest.mark.asyncio
async def test_german_word_order():
    result = await get_feedback(
        FeedbackRequest(
            sentence="Ich habe gegessen gestern Pizza.",
            target_language="German",
            native_language="English",
        )
    )
    assert result.is_correct is False
    assert len(result.errors) >= 1
    assert result.difficulty in VALID_DIFFICULTIES
    for error in result.errors:
        assert error.error_type in VALID_ERROR_TYPES


# Testing high complexity correct sentence - difficulty should be C1 or C2
@pytest.mark.asyncio
async def test_high_complexity_correct_sentence():
    result = await get_feedback(
        FeedbackRequest(
            sentence="Notwithstanding the considerable advancements in artificial intelligence, the nuanced complexities of human cognition remain, for the most part, beyond the reach of current computational models.",
            target_language="English",
            native_language="English",
        )
    )
    assert result.is_correct is True
    assert result.errors == []
    assert result.difficulty in {"C1", "C2"}
