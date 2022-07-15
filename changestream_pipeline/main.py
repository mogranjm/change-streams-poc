import datetime
from typing import List

from google.cloud import spanner
from google.cloud.spanner_v1.streamed import StreamedResultSet
from config import SPANNER_INSTANCE, SPANNER_DATABASE

from ChangeRecords import DataChangeRecord, HeartbeatRecord, ChildPartitionRecord

TIMESTAMP_STRING = "%Y-%m-%dT%H:%M:%S.%fZ"


def query_changestream(database, start: datetime, end: datetime = None, heartbeat: int = 10000, partition_token: str = None):

    end = f"'{end.strftime(TIMESTAMP_STRING)}'" if end is not None else "NULL"

    partition_token = f"'{partition_token}'" if partition_token is not None else "NULL"

    with database.snapshot() as snapshot:
        results: StreamedResultSet = snapshot.execute_sql(
            "SELECT ChangeRecord FROM READ_test_stream("
                f"start_timestamp => '{start.strftime(TIMESTAMP_STRING)}',"
                f"end_timestamp => {end},"
                f"heartbeat_milliseconds => {heartbeat},"
                f"partition_token => {partition_token}"
            ");"
        )

    return results


def process_changestream() -> List:
    wrench = spanner.Client()
    instance = wrench.instance(SPANNER_INSTANCE)
    db = instance.database(SPANNER_DATABASE)

    start_time = datetime.datetime.utcnow() - datetime.timedelta(minutes=5)

    # Initiate Read Window (get Change Stream head)
    stream_head = query_changestream(db, start_time)

    # Get child tokens from stream head
    child_tokens = [child_record[0][0][2][0][2][0][0] for child_record in stream_head]

    # Requery for child partitions
    child_partitions = [query_changestream(db, start_time, partition_token=token) for token in child_tokens]

    # This one takes a while
    data_change_records = [[record for record in stream] for stream in child_partitions]

    processed_records = []
    for partition in data_change_records:
        if partition[0][0][0][0] != []:
            # Data change record
            new_record = DataChangeRecord(partition[0][0][0][0])
        elif partition[0][0][0][1] == []:
            # heartbeat record
            new_record = HeartbeatRecord(partition[0][0][0][1])
        else:
            # child_partition_record
            new_record = ChildPartitionRecord(partition[0][0][0][2])
        processed_records.append(new_record)

    return processed_records

if __name__ == '__main__':
    recs = process_changestream()
    print(recs)
