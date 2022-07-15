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
