import json
import boto3
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
status_table = dynamodb.Table('PackageStatus')
history_table = dynamodb.Table('PackageEventHistory')

def lambda_handler(event, context):
    for record in event.get('Records', [event]):
        if 'body' in record:
            body = json.loads(record['body'])
        else:
            body = record

        package_id = body['packageId']
        event_id = body['eventId']
        status = body['status']
        event_timestamp = int(body['eventTimestamp'])

        print(f"DEBUG: package_id={package_id!r} type={type(package_id)}, event_timestamp={event_timestamp!r} type={type(event_timestamp)}")

        existing = history_table.get_item(
            Key={'packageId': package_id, 'eventTimestamp': event_timestamp}
        )
        if 'Item' in existing and existing['Item'].get('eventId') == event_id:
            print(f"DUPLICATE event dropped: {event_id} for package {package_id}")
            continue

        history_table.put_item(Item={
            'packageId': package_id,
            'eventTimestamp': event_timestamp,
            'eventId': event_id,
            'status': status,
            'processed': True
        })

        current = status_table.get_item(Key={'packageId': package_id})

        if 'Item' in current:
            last_timestamp = int(current['Item'].get('lastEventTimestamp', 0))
            if event_timestamp <= last_timestamp:
                print(f"STALE event dropped: package {package_id}, incoming_ts={event_timestamp}, stored_ts={last_timestamp}")
                continue

        status_table.put_item(Item={
            'packageId': package_id,
            'currentStatus': status,
            'lastEventTimestamp': event_timestamp,
            'lastUpdated': datetime.utcnow().isoformat()
        })
        print(f"STATUS UPDATED: package {package_id} -> {status}")

    return {'statusCode': 200, 'body': json.dumps('Processing complete')}