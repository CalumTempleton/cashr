CATEGORIES = [
    "Food & juice",
    "Alcohol",
    "Health & hygiene",
    "Travel",
    "Sports & leisure",
    "Presents & gifts",
    "Flat",
    "Utilities",
    "Other",
]

COLUMN_KEYS = ["date", "category", "description", "balance", "value"]
HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}

LONG_DESCRIPTION = (
    "This is a really long description that will exceed the character limit. "
    "The character limited was added in to make sure the description does not "
    "exceed VARCHAR255 which is a good idea. Without this check, the database "
    "not accept the data, therefore causing the software to crash. Note the "
    "character limit has been set to 250 to be on the safe side."
)
