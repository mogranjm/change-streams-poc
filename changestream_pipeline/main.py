import datetime
from google.cloud import spanner
from google.cloud.spanner_v1.streamed import StreamedResultSet
from config import SPANNER_INSTANCE, SPANNER_DATABASE

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


def process_changestream():
    wrench = spanner.Client()
    instance = wrench.instance(SPANNER_INSTANCE)
    db = instance.database(SPANNER_DATABASE)

    start_time = datetime.datetime.utcnow() - datetime.timedelta(minutes=5)

    # Initiate Read Window (get Change Stream head)
    stream_head = query_changestream(db, start_time)

    # Get child tokens from stream head
    child_tokens = [child_record[0][0][2][0][2][0][0] for child_record in stream_head]

    # Get child partitions
    child_partitions = [query_changestream(db, start_time, partition_token=token) for token in child_tokens]

    data_change_records = [[record for record in stream] for stream in child_partitions]

    return data_change_records

if __name__ == '__main__':
    recs = process_changestream()
    print(recs)
