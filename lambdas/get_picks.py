import boto3
import json

def get_bowl_picks_table():
    table_name = 'bowl-picks'
    dynamo_resource = boto3.resource('dynamodb')
    return dynamo_resource.Table(table_name)
    
    
def get_bowl_picks():
    bowl_picks_table = get_bowl_picks_table()
    table_scan = bowl_picks_table.scan()
    return table_scan['Items']
    
def lambda_handler(event, context):
    bowl_picks = get_bowl_picks()
    return bowl_picks
