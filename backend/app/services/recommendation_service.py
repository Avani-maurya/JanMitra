from backend.app.database.rule_repository import get_rule_by_scheme_id
from backend.app.database.scheme_repository import get_all_active_schemes
from backend.app.models.eligibility_rule import EligibilityRule
from backend.app.models.user import User
from backend.app.services.eligibility_service import evaluate_rule_with_details


def get_recommendations(user: User) -> list[dict]:
    recommendations = []

    schemes = get_all_active_schemes()

    for scheme in schemes:
        rule_data = get_rule_by_scheme_id(scheme["id"])

        if not rule_data:
            continue

        rule = EligibilityRule(**rule_data)

        result = evaluate_rule_with_details(user, rule)

        if result["eligible"]:
            recommendations.append(
                {
                    "scheme_id": scheme["id"],
                    "name": scheme["name"],
                    "description": scheme["description"],
                    "category": scheme["category"],
                    "level": scheme["level"],
                    "benefits": scheme["benefits"],
                    "application_url": scheme["application_url"],
                    "match_details": result["conditions"],
                }
            )

    return recommendations