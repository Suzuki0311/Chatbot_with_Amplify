import json
from . import aws_systems_manager
from . import const


def handler(event, context):
  print('received event:')
  print(event)

  if event['type'] == 'checkout.session.completed':
    session = event['data']['object']
    line_user_id = session['client_reference_id']
    customer_id = session['customer']

  
  return {
      'statusCode': 200,
      'headers': {
          'Access-Control-Allow-Headers': '*',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
      },
      'body': json.dumps('Hello from your new Amplify Python lambda!')
  }