pet = {
    "type": "object",
    "required": ["name", "type"],
    "properties": {
        "id": {
            "type": "integer",
            "enum":[0,1,2]
        },
        "name": {
            "type": "string",
            "enum":["snowball","ranger","flippy"]
        },
        "type": {
            "type": "string",
            "enum": ["cat", "dog", "fish"]
        },
        "status": {
            "type": "string",
            "enum": ["available","sold","pending"]
        },
    }
}
