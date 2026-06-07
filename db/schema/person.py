def person_schema(person) -> dict:
    return {"id": str(person["_id"]),
            "name": person["name"],
            "number": person["number"]}


def persons_schema(persons) -> list:
    return [person_schema(person) for person in persons]