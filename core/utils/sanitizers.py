from __future__ import annotations

import re


def sanitize_input(text: str) -> str:
    text = text.strip()
    text = re.sub(r'<script[^>]*>.*?</script>', '', text, flags=re.IGNORECASE | re.DOTALL)
    return text


def sanitize_path_component(component: str) -> str:
    return re.sub(r'[^\w\-_\. ]', '', component)
