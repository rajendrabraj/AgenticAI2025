import json
from typing import TypedDict, List, Dict, Any


def to_json(s: str) -> Any:
    s = s.strip()
    if s.startswith("```"):
        s = s.split("```", 2)[1]
        s = s.replace("json", "", 1).strip()
    return json.loads(s)


