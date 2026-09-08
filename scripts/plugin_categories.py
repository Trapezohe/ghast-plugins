"""Store categories; old manifest values remain supported for installed packages."""
CATEGORY_ALIASES = {
    "databases": "data",
    "data-analytics": "data",
    "development": "developer-tools",
    "creativity": "creative",
    "design": "creative",
}
CATEGORIES = {
    "business", "communication", "creative", "data", "developer-tools",
    "finance", "gaming", "information", "lifestyle", "marketing", "media",
    "news", "other", "productivity", "research", "system", "utility", "web",
}


def plugin_category(value):
    category = CATEGORY_ALIASES.get(value, value)
    if category not in CATEGORIES:
        raise ValueError(f"Unknown plugin category: {value!r}")
    return category
