from dataclasses import dataclass
from typing import List, Dict
import datetime


@dataclass()
class ChangeRecord:
    timestamp: datetime


class DataChangeRecord(ChangeRecord):
    record_sequence: str
    transaction_id: str
    is_last_record_in_transaction_partition: bool
    table_name: str
    column_types: List[Dict[str, str, bool, int]]
    changed_values: List[Dict[Dict, Dict, Dict]]
    change_type: str
    value_capture_type: str
    records_in_transaction: int
    partitions_in_transaction: int


class ChildPartitionRecord(ChangeRecord):
    record_sequence: str
    child_partitions: List[Dict[str, List[str]]]
