from typing import Any

from backend.app.models.eligibility_rule import EligibilityRule
from backend.app.models.user import User


def get_field_value(user: User, field: str) -> Any:
    return getattr(user, field, None)


def evaluate_condition(
    user: User,
    field: str,
    operator: str,
    expected: Any
) -> bool:
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


def get_condition_status(
    user: User,
    field: str,
    operator: str,
    expected: Any
) -> tuple[str, Any]:
    actual = get_field_value(user, field)

    if actual is None:
        return "UNKNOWN", actual

    matched = evaluate_condition(
        user,
        field,
        operator,
        expected,
    )

    return ("MATCHED" if matched else "NOT_MATCHED"), actual


def combine_statuses(statuses: list[str], logic: str) -> str:
    if logic == "AND":
        if "NOT_MATCHED" in statuses:
            return "NOT_MATCHED"

        if "UNKNOWN" in statuses:
            return "UNKNOWN"

        return "MATCHED"

    if logic == "OR":
        if "MATCHED" in statuses:
            return "MATCHED"

        if "UNKNOWN" in statuses:
            return "UNKNOWN"

        return "NOT_MATCHED"

    raise ValueError(f"Unsupported rule logic: {logic}")


def evaluate_rule_with_details(user: User, rule: EligibilityRule) -> dict:
    results = []
    statuses = []

    for condition in rule.conditions:
        status, actual = get_condition_status(
            user,
            condition.field,
            condition.operator,
            condition.value,
        )

        statuses.append(status)

        results.append(
            {
                "field": condition.field,
                "operator": condition.operator,
                "expected": condition.value,
                "actual": actual,
                "matched": status == "MATCHED",
                "status": status,
            }
        )

    overall_status = combine_statuses(statuses, rule.logic)

    return {
        "eligible": overall_status == "MATCHED",
        "status": overall_status,
        "conditions": results,
    }