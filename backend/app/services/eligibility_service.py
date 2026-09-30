from typing import Any

from backend.app.models.eligibility_rule import EligibilityRule
from backend.app.models.user import User


def get_field_value(user: User, field: str) -> Any:
    return getattr(user, field, None)


def evaluate_condition(user: User, field: str, operator: str, expected: Any) -> bool:
    actual = get_field_value(user, field)

    if actual is None:
        return False

    if operator == "==":
        return actual == expected

    if operator == "!=":
        return actual != expected

    if operator == ">":
        return actual > expected

    if operator == ">=":
        return actual >= expected

    if operator == "<":
        return actual < expected

    if operator == "<=":
        return actual <= expected

    if operator == "in":
        return actual in expected

    if operator == "not_in":
        return actual not in expected

    raise ValueError(f"Unsupported operator: {operator}")


def evaluate_rule(user: User, rule: EligibilityRule) -> bool:
    results = [
        evaluate_condition(
            user,
            condition.field,
            condition.operator,
            condition.value,
        )
        for condition in rule.conditions
    ]

    if rule.logic == "AND":
        return all(results)

    if rule.logic == "OR":
        return any(results)

    raise ValueError(f"Unsupported rule logic: {rule.logic}")

def evaluate_rule_with_details(user: User, rule: EligibilityRule) -> dict:
    results = []

    for condition in rule.conditions:
        actual = get_field_value(user, condition.field)

        if actual is None:
            matched = False
        else:
            matched = evaluate_condition(
                user,
                condition.field,
                condition.operator,
                condition.value,
            )

        results.append(
            {
                "field": condition.field,
                "operator": condition.operator,
                "expected": condition.value,
                "actual": actual,
                "matched": matched,
            }
        )

    if rule.logic == "AND":
        eligible = all(item["matched"] for item in results)
    else:
        eligible = any(item["matched"] for item in results)

    return {
        "eligible": eligible,
        "conditions": results,
    }
