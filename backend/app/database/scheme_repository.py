from .connection import db


schemes_collection = db["schemes"]


def get_all_active_schemes():
    return list(
        schemes_collection.find(
            {"status": "active"},
            {"_id": 0}
        )
    )


def get_scheme_by_id(scheme_id: str):
    return schemes_collection.find_one(
        {"id": scheme_id},
        {"_id": 0}
    )


def insert_scheme(scheme: dict):
    return schemes_collection.insert_one(scheme)