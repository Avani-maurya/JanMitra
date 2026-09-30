from backend.app.models.user import User
from backend.app.services import recommendation_service


def test_matched_scheme_goes_to_recommendations(monkeypatch):
    scheme = {
        "id": "scheme_test",
        "name": "Test Scheme",
        "description": "Test description",
        "category": "Agriculture",
        "level": "Central",
        "benefits": ["Test benefit"],
        "application_url": "https://example.com",
    }

    rule = {
        "id": "rule_test",
        "scheme_id": "scheme_test",
        "conditions": [
            {
                "field": "is_farmer",
                "operator": "==",
                "value": True,
            }
        ],
        "logic": "AND",
    }

    monkeypatch.setattr(
        recommendation_service,
        "get_all_active_schemes",
        lambda: [scheme],
    )

    monkeypatch.setattr(
        recommendation_service,
        "get_rule_by_scheme_id",
        lambda scheme_id: rule,
    )

    user = User(
        name="Eligible User",
        age=30,
        state="Uttar Pradesh",
        is_farmer=True,
    )

    result = recommendation_service.get_recommendations(user)

    assert len(result["recommendations"]) == 1
    assert result["recommendations"][0]["scheme_id"] == "scheme_test"
    assert result["recommendations"][0]["match_status"] == "MATCHED"
    assert result["needs_more_information"] == []


def test_unknown_scheme_goes_to_needs_more_information(monkeypatch):
    scheme = {
        "id": "scheme_test",
        "name": "Test Scheme",
        "description": "Test description",
        "category": "Agriculture",
        "level": "Central",
        "benefits": ["Test benefit"],
        "application_url": "https://example.com",
    }

    rule = {
        "id": "rule_test",
        "scheme_id": "scheme_test",
        "conditions": [
            {
                "field": "landholding_status",
                "operator": "==",
                "value": True,
            }
        ],
        "logic": "AND",
    }

    monkeypatch.setattr(
        recommendation_service,
        "get_all_active_schemes",
        lambda: [scheme],
    )

    monkeypatch.setattr(
        recommendation_service,
        "get_rule_by_scheme_id",
        lambda scheme_id: rule,
    )

    user = User(
        name="Incomplete User",
        age=30,
        state="Uttar Pradesh",
        is_farmer=True,
    )

    result = recommendation_service.get_recommendations(user)

    assert result["recommendations"] == []
    assert len(result["needs_more_information"]) == 1
    assert (
        result["needs_more_information"][0]["match_status"]
        == "UNKNOWN"
    )


def test_not_matched_scheme_is_not_recommended(monkeypatch):
    scheme = {
        "id": "scheme_test",
        "name": "Test Scheme",
        "description": "Test description",
        "category": "Agriculture",
        "level": "Central",
        "benefits": ["Test benefit"],
        "application_url": "https://example.com",
    }

    rule = {
        "id": "rule_test",
        "scheme_id": "scheme_test",
        "conditions": [
            {
                "field": "is_farmer",
                "operator": "==",
                "value": True,
            }
        ],
        "logic": "AND",
    }

    monkeypatch.setattr(
        recommendation_service,
        "get_all_active_schemes",
        lambda: [scheme],
    )

    monkeypatch.setattr(
        recommendation_service,
        "get_rule_by_scheme_id",
        lambda scheme_id: rule,
    )

    user = User(
        name="Ineligible User",
        age=30,
        state="Uttar Pradesh",
        is_farmer=False,
    )

    result = recommendation_service.get_recommendations(user)

    assert result["recommendations"] == []
    assert result["needs_more_information"] == []

    
    
def test_multiple_matching_schemes_are_returned(monkeypatch):
    schemes = [
        {
            "id": "scheme_one",
            "name": "Scheme One",
            "description": "First test scheme",
            "category": "Agriculture",
            "level": "Central",
            "benefits": ["Benefit one"],
            "application_url": "https://example.com/one",
        },
        {
            "id": "scheme_two",
            "name": "Scheme Two",
            "description": "Second test scheme",
            "category": "Agriculture",
            "level": "Central",
            "benefits": ["Benefit two"],
            "application_url": "https://example.com/two",
        },
    ]

    rules = {
        "scheme_one": {
            "id": "rule_one",
            "scheme_id": "scheme_one",
            "conditions": [
                {
                    "field": "is_farmer",
                    "operator": "==",
                    "value": True,
                }
            ],
            "logic": "AND",
        },
        "scheme_two": {
            "id": "rule_two",
            "scheme_id": "scheme_two",
            "conditions": [
                {
                    "field": "landholding_status",
                    "operator": "==",
                    "value": True,
                }
            ],
            "logic": "AND",
        },
    }

    monkeypatch.setattr(
        recommendation_service,
        "get_all_active_schemes",
        lambda: schemes,
    )

    monkeypatch.setattr(
        recommendation_service,
        "get_rule_by_scheme_id",
        lambda scheme_id: rules[scheme_id],
    )

    user = User(
        name="Farmer User",
        age=35,
        state="Uttar Pradesh",
        is_farmer=True,
        landholding_status=True,
    )

    result = recommendation_service.get_recommendations(user)

    assert len(result["recommendations"]) == 2
    assert result["recommendations"][0]["scheme_id"] == "scheme_one"
    assert result["recommendations"][1]["scheme_id"] == "scheme_two"
    assert result["needs_more_information"] == []

def test_disability_scholarship_goes_to_recommendations(monkeypatch):
    scheme = {
        "id": "scheme_pre_matric_disability",
        "name": "Pre-Matric Scholarship for Students with Disabilities",
        "description": "Scholarship support for eligible students.",
        "category": "Education",
        "level": "Central",
        "benefits": ["Scholarship assistance"],
        "application_url": "https://scholarships.gov.in/",
    }

    rule = {
        "id": "rule_pre_matric_disability",
        "scheme_id": "scheme_pre_matric_disability",
        "conditions": [
            {
                "field": "is_student",
                "operator": "==",
                "value": True,
            },
            {
                "field": "school_class",
                "operator": ">=",
                "value": 9,
            },
            {
                "field": "school_class",
                "operator": "<=",
                "value": 10,
            },
            {
                "field": "is_disabled",
                "operator": "==",
                "value": True,
            },
            {
                "field": "disability_percentage",
                "operator": ">=",
                "value": 40,
            },
            {
                "field": "annual_income",
                "operator": "<=",
                "value": 250000,
            },
        ],
        "logic": "AND",
    }

    monkeypatch.setattr(
        recommendation_service,
        "get_all_active_schemes",
        lambda: [scheme],
    )

    monkeypatch.setattr(
        recommendation_service,
        "get_rule_by_scheme_id",
        lambda scheme_id: rule,
    )

    user = User(
        name="Scholarship User",
        age=15,
        state="Uttar Pradesh",
        is_student=True,
        school_class=9,
        is_disabled=True,
        disability_percentage=50,
        annual_income=150000,
    )

    result = recommendation_service.get_recommendations(user)

    assert len(result["recommendations"]) == 1
    assert (
        result["recommendations"][0]["scheme_id"]
        == "scheme_pre_matric_disability"
    )
    assert (
        result["recommendations"][0]["match_status"]
        == "MATCHED"
    )
    assert result["needs_more_information"] == []


def test_disability_scholarship_needs_more_information(monkeypatch):
    scheme = {
        "id": "scheme_pre_matric_disability",
        "name": "Pre-Matric Scholarship for Students with Disabilities",
        "description": "Scholarship support for eligible students.",
        "category": "Education",
        "level": "Central",
        "benefits": ["Scholarship assistance"],
        "application_url": "https://scholarships.gov.in/",
    }

    rule = {
        "id": "rule_pre_matric_disability",
        "scheme_id": "scheme_pre_matric_disability",
        "conditions": [
            {
                "field": "is_student",
                "operator": "==",
                "value": True,
            },
            {
                "field": "school_class",
                "operator": ">=",
                "value": 9,
            },
            {
                "field": "school_class",
                "operator": "<=",
                "value": 10,
            },
            {
                "field": "is_disabled",
                "operator": "==",
                "value": True,
            },
            {
                "field": "disability_percentage",
                "operator": ">=",
                "value": 40,
            },
            {
                "field": "annual_income",
                "operator": "<=",
                "value": 250000,
            },
        ],
        "logic": "AND",
    }

    monkeypatch.setattr(
        recommendation_service,
        "get_all_active_schemes",
        lambda: [scheme],
    )

    monkeypatch.setattr(
        recommendation_service,
        "get_rule_by_scheme_id",
        lambda scheme_id: rule,
    )

    user = User(
        name="Incomplete Student",
        age=15,
        state="Uttar Pradesh",
        is_student=True,
        school_class=9,
        is_disabled=True,
    )

    result = recommendation_service.get_recommendations(user)

    assert result["recommendations"] == []
    assert len(result["needs_more_information"]) == 1
    assert (
        result["needs_more_information"][0]["match_status"]
        == "UNKNOWN"
    )


def test_disability_scholarship_not_recommended_when_disability_is_below_threshold(
    monkeypatch,
):
    scheme = {
        "id": "scheme_pre_matric_disability",
        "name": "Pre-Matric Scholarship for Students with Disabilities",
        "description": "Scholarship support for eligible students.",
        "category": "Education",
        "level": "Central",
        "benefits": ["Scholarship assistance"],
        "application_url": "https://scholarships.gov.in/",
    }

    rule = {
        "id": "rule_pre_matric_disability",
        "scheme_id": "scheme_pre_matric_disability",
        "conditions": [
            {
                "field": "is_student",
                "operator": "==",
                "value": True,
            },
            {
                "field": "school_class",
                "operator": ">=",
                "value": 9,
            },
            {
                "field": "school_class",
                "operator": "<=",
                "value": 10,
            },
            {
                "field": "is_disabled",
                "operator": "==",
                "value": True,
            },
            {
                "field": "disability_percentage",
                "operator": ">=",
                "value": 40,
            },
            {
                "field": "annual_income",
                "operator": "<=",
                "value": 250000,
            },
        ],
        "logic": "AND",
    }

    monkeypatch.setattr(
        recommendation_service,
        "get_all_active_schemes",
        lambda: [scheme],
    )

    monkeypatch.setattr(
        recommendation_service,
        "get_rule_by_scheme_id",
        lambda scheme_id: rule,
    )

    user = User(
        name="Ineligible Student",
        age=15,
        state="Uttar Pradesh",
        is_student=True,
        school_class=9,
        is_disabled=True,
        disability_percentage=30,
        annual_income=150000,
    )

    result = recommendation_service.get_recommendations(user)

    assert result["recommendations"] == []
    assert result["needs_more_information"] == []
