from dataclasses import dataclass


@dataclass
class Entity:

    entity_type: str

    value: str

    source: str

    confidence: float = 1.0