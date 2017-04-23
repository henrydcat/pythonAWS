import boto3 

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
        'launchTime':instance.launch_time, 'instanceId':instance.instance_id,
        'region':region
      }  
      list.append(ec2info)

  return list

#----

