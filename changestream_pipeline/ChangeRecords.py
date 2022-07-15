from dataclasses import dataclass
from typing import List, Dict
import datetime


@dataclass()
class ChangeRecord:
    timestamp: datetime
