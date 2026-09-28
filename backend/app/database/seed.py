import json
from pathlib import Path

from .connection import db


BASE_DIR = Path(__file__).resolve().parents[3]
DATA_DIR = BASE_DIR / "data"


def load_json(filename: str) -> dict:
    with open(DATA_DIR / filename, "r", encoding="utf-8") as file:
        return json.load(file)


def seed_schemes():
    data = load_json("government_schemes.json")

    for scheme in data["schemes"]:
        db.schemes.update_one(
            {"id": scheme["id"]},
            {"$set": scheme},
            upsert=True,
        )

    print(f"Seeded {len(data['schemes'])} scheme(s)")


def seed_eligibility_rules():
    data = load_json("eligibility_rules.json")

    for rule in data["eligibility_rules"]:
        db.eligibility_rules.update_one(
            {"id": rule["id"]},
            {"$set": rule},
            upsert=True,
        )

    print(f"Seeded {len(data['eligibility_rules'])} eligibility rule(s)")


def seed_all():
    seed_schemes()
    seed_eligibility_rules()


if __name__ == "__main__":
    seed_all()