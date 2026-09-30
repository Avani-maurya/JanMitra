from .connection import db


rules_collection = db["eligibility_rules"]


def get_rule_by_id(rule_id: str):
    return rules_collection.find_one(
        {"id": rule_id},
        {"_id": 0}
    )


def get_rule_by_scheme_id(scheme_id: str):
    return rules_collection.find_one(
        {"scheme_id": scheme_id},
        {"_id": 0}
    )


def insert_rule(rule: dict):
    return rules_collection.insert_one(rule)