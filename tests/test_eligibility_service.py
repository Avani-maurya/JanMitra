import pytest
from pydantic import ValidationError

from backend.app.models.eligibility_rule import EligibilityRule
from backend.app.models.user import User
from backend.app.services.eligibility_service import evaluate_rule_with_details


def create_rule(logic="AND"):
    return EligibilityRule(
        id="rule_test",
        scheme_id="scheme_test",
        conditions=[
            {
                "field": "is_farmer",
                "operator": "==",
                "value": True,
            },
            {
                "field": "landholding_status",
                "operator": "==",
                "value": True,
            },
        ],
        logic=logic,
    )


def test_all_conditions_match():
    user = User(
        name="Eligible User",
        age=30,
        state="Uttar Pradesh",
        is_farmer=True,
        landholding_status=True,
    )

    result = evaluate_rule_with_details(user, create_rule())

    assert result["eligible"] is True
    assert result["status"] == "MATCHED"


def test_one_condition_does_not_match():
    user = User(
        name="Ineligible User",
        age=30,
        state="Uttar Pradesh",
        is_farmer=True,
        landholding_status=False,
    )

    result = evaluate_rule_with_details(user, create_rule())

    assert result["eligible"] is False
    assert result["status"] == "NOT_MATCHED"


def test_missing_information_is_unknown():
    user = User(
        name="Incomplete User",
        age=30,
        state="Uttar Pradesh",
        is_farmer=True,
    )

    result = evaluate_rule_with_details(user, create_rule())

    assert result["eligible"] is False
    assert result["status"] == "UNKNOWN"


def test_or_logic_matches_if_any_condition_matches():
    user = User(
        name="OR User",
        age=30,
        state="Uttar Pradesh",
        is_farmer=True,
        landholding_status=False,
    )

    result = evaluate_rule_with_details(user, create_rule(logic="OR"))

    assert result["eligible"] is True
    assert result["status"] == "MATCHED"

def test_negative_age_is_rejected():
    with pytest.raises(ValidationError):
        User(
            name="Invalid User",
            age=-1,
            state="Uttar Pradesh",
        )


def test_age_above_120_is_rejected():
    with pytest.raises(ValidationError):
        User(
            name="Invalid User",
            age=121,
            state="Uttar Pradesh",
        )


def test_negative_income_is_rejected():
    with pytest.raises(ValidationError):
        User(
            name="Invalid User",
            age=30,
            state="Uttar Pradesh",
            annual_income=-1000,
        )


def test_disability_percentage_above_100_is_rejected():
    with pytest.raises(ValidationError):
        User(
            name="Invalid User",
            age=30,
            state="Uttar Pradesh",
            disability_percentage=101,
        )