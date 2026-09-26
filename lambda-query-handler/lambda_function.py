import json
import boto3
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
status_table = dynamodb.Table('PackageStatus')
history_table = dynamodb.Table('PackageEventHistory')

def decimal_default(obj):
    if isinstance(obj, Decimal):
        return int(obj) if obj % 1 == 0 else float(obj)
    raise TypeError

def response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(body, default=decimal_default)
    }

def lambda_handler(event, context):
    http_method = event.get('httpMethod')
    path_params = event.get('pathParameters') or {}
    package_id = path_params.get('packageId')
    resource_path = event.get('resource', '')

    print(f"DEBUG: method={http_method}, resource={resource_path}, packageId={package_id}")

    try:
        if http_method == 'GET' and resource_path.endswith('/status'):
            result = status_table.get_item(Key={'packageId': package_id})
            if 'Item' not in result:
                return response(404, {'error': 'Package not found'})
            return response(200, result['Item'])

        elif http_method == 'GET' and resource_path.endswith('/history'):
            result = history_table.query(
                KeyConditionExpression=boto3.dynamodb.conditions.Key('packageId').eq(package_id)
            )
            return response(200, {'packageId': package_id, 'events': result.get('Items', [])})

        elif http_method == 'GET' and resource_path.rstrip('/').endswith('/packages'):
            result = status_table.scan()
            return response(200, {'packages': result.get('Items', [])})

        elif http_method == 'DELETE':
            status_table.delete_item(Key={'packageId': package_id})
            print(f"DELETED: package {package_id}")
            return response(200, {'message': f'Package {package_id} deleted'})

        else:
            return response(400, {'error': 'Unsupported route'})

    except Exception as e:
        print(f"ERROR: {str(e)}")
        return response(500, {'error': str(e)})