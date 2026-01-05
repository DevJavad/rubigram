from __future__ import annotations

from typing import Union, Any
import rubigram

def clean_payload(data: dict):
    return {
        key: value for key, value in data.items() if value is not None
    }