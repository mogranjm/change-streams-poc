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

    # TEMP data_change_record EXTRACTION LOGIC - these indices are not replicated each time the stream is queried
    #       logic above checks for ChangeRecord type
    # dcr[0]: heartbeat records
    # dcr[1]: child_partition_records
    # dcr[2]: actual data_change_recards
    for i in data_change_records[2]:
        print('|--RECORD--|')
        try:
            print([{
                'timestamp': j[0],
                'record_sequence': j[1],
                'transaction_id': j[2],
                'is_last_record_in_transaction_in_partition': j[3],
                'table_name': j[4],
                'column_types': [
                    {
                        'name': type[0],
                        'type': type[1]['code'],
                        'is_primary_key': type[2],
                        'ordinal_position': type[3]
                    }
                    for type in j[5]
                ],
                'changed_values': [
                    {
                        'key': value[0],
                        'new_values': value[1],
                        'old_values': value[2]
                    } for value in j[6]
                ],
                'change_type': j[7],
                'value_capture_type': j[8],
                'records_in_transaction': j[9],
                'partitions_in_transaction': j[10]
            } for j in i[0][0][0]]
            )
        except IndexError:
            pass

    return processed_records

if __name__ == '__main__':
    recs = process_changestream()
    print(recs)
