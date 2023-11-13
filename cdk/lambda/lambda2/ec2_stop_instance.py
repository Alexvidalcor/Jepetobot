# Libraries import
import json
import boto3
 
#Main vars
region = 'REPLACEREGION'
envDeploy = 'REPLACEENVDEPLOY'
appName = 'REPLACEAPPNAME'

customFilter = [{
    'Name':'tag:Name', 
    'Values': [appName + "-" + envDeploy + "_instance"]
}]
    

# Client definition
ec2 = boto3.client('ec2', region_name=region)

# Search instances (TODO: Currently only one instance is detected. Multiple instances support is needed)
instancesList = []
locateEc2Filtered = ec2.describe_instances(Filters=customFilter)
idEc2Filtered = locateEc2Filtered["Reservations"][0]["Instances"][0]["InstanceId"]
instancesList.append(idEc2Filtered)

# Logic
def ec2_stop_function(event, context):
    ec2.stop_instances(InstanceIds=instancesList)
    print(f"Starting instance: {idEc2Filtered}")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Success')
    }



