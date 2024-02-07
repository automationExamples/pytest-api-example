pet = {
    "type": "object",
    "required": ["name", "type"],
    "properties": {
        "id": {
            "type": "integer"
        },
        "name": {
            "type": "string"
        },
        "type": {
            "type": "string",
            "enum": ["cat", "dog", "fish"]
        },
        "status": {
            "type": "string",
            "enum": ["available", "sold", "pending"]
        }
    }
}

Order = {
    "type": "object",
    "properties": {
        "id": {"type": "integer"},
        "pet_id": {"type": "integer"}
    },
    "required": ["pet_id"]
}


OrderUpdate = {
    "type": "object",
    "properties": {
        "status": {"type": "string"}
    }
}