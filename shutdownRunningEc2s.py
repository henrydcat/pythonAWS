import boto3
import json

def runningEc2s (): #returns running Ec2's for all regions
  client = boto3.client('ec2')
  regions = client.describe_regions()['Regions']
  list=[]
  for region in regions:
    region_name=region['RegionName']
    ec2 = boto3.resource('ec2',region_name=region['RegionName'])
    running_instances = ec2.instances.filter(Filters=[{
      'Name': 'instance-state-name', 'Values': ['running']}])
    ec2info = {}
    for instance in running_instances:
      #get Name of instance if any
      for tag in instance.tags:
        if 'Name' in tag['Key']:
          name=tag['Value']
      #make instance dict:
      ec2info={
        'name':name, 'type':instance.instance_type, 'state':instance.state['Name'],
        'privateIp':instance.private_ip_address, 'publicIp':instance.public_ip_address,
        'instanceId':instance.instance_id, 'region':region
      }
      list.append(ec2info)

  return list
#----
def stopInstance(instanceId, region):
  ec2=boto3.client('ec2', region_name=region)
  response=ec2.stop_instances(InstanceIds=instanceId)
  print "Stopped instance %s" %(instanceId)
  return response
#---

runningList=runningEc2s()

for instance in runningList:
  #response=stopInstance(instanceId['instanceId'], instance['region'])
  print json.dumps(instance, indent=2)

