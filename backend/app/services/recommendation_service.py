from backend.app.database.rule_repository import get_rule_by_scheme_id
from backend.app.database.scheme_repository import get_all_active_schemes
from backend.app.models.eligibility_rule import EligibilityRule
from backend.app.models.user import User
from backend.app.services.eligibility_service import evaluate_rule_with_details


def build_scheme_result(scheme: dict, result: dict) -> dict:
    return {
        "scheme_id": scheme["id"],
        "name": scheme["name"],
        "description": scheme["description"],
        "category": scheme["category"],
        "level": scheme["level"],
        "benefits": scheme["benefits"],
        "application_url": scheme["application_url"],
        "match_status": result["status"],
        "match_details": result["conditions"],
    }


def get_recommendations(user: User) -> dict:
    recommendations = []
    needs_more_information = []

    schemes = get_all_active_schemes()

    for scheme in schemes:
        rule_data = get_rule_by_scheme_id(scheme["id"])

        if not rule_data:
            continue

        rule = EligibilityRule(**rule_data)

        result = evaluate_rule_with_details(user, rule)

        scheme_result = build_scheme_result(scheme, result)

        if result["status"] == "MATCHED":
            recommendations.append(scheme_result)

        elif result["status"] == "UNKNOWN":
            needs_more_information.append(scheme_result)

    return {
        "recommendations": recommendations,
        "needs_more_information": needs_more_information,
    }