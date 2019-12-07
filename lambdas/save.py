import boto3
import json
from uuid import uuid4


def get_table_name():
    return 'bowl-picks'
    
    
def get_bowl_picks_table():
    table_name = get_table_name()
    dynamodb = boto3.resource('dynamodb')
    return dynamodb.Table(table_name)


def get_bowl_picks_from_event(event):
    return event


def add_id_to_bowl_picks(bowl_picks):
    id = str(uuid4())
    bowl_picks['id'] = id


def save_bowl_picks(bowl_picks):
    table = get_bowl_picks_table()
    table.put_item(
        Item=bowl_picks    
    )
    
    
def build_response(error=None):
    message = error or 'Saved'
    status_code = 400 if error else 200
    return {
        'statusCode': status_code,
        'body': message
    }
    
    
def lambda_handler(event, context):
    try:
        print(f'EVENT {event}')
        bowl_picks = get_bowl_picks_from_event(event)
        add_id_to_bowl_picks(bowl_picks)
        print(f'Bowl picks: {bowl_picks}')
        save_bowl_picks(bowl_picks)
        return build_response()
    except:
        return build_response('Couldn\'t Save')