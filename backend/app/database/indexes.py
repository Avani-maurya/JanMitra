from .connection import db


def create_indexes():
    db.users.create_index("id", unique=True)
    db.schemes.create_index("id", unique=True)
    db.schemes.create_index("category")
    db.schemes.create_index("state")
    db.schemes.create_index("status")
    db.eligibility_rules.create_index("id", unique=True)
    db.eligibility_rules.create_index("scheme_id", unique=True)
    db.recommendations.create_index("user_id")