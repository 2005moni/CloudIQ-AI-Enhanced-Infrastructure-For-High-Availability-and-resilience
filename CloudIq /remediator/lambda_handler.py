
import boto3
def lambda_handler(event, context):
    ecs = boto3.client('ecs')
    ecs.update_service(
        cluster='myCluster',
        service='frontend',
        desiredCount=3
    )
    return {"message": "Frontend scaled from Lambda"}
