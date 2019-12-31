import boto3
import botocore
import click

session = boto3.session.Session(profile_name='shotty')
ec2 = session.resource('ec2')

def get_instances(project):
    instances = []
    if project:
        filters = [{'Name':'tag:Project', 'Values':[project]}]
        instances = ec2.instances.filter(Filters=filters)
    else:
        instances = ec2.instances.all()  
    return instances 

@click.group()
def cli():
    """Shotty manages shapshotting"""

@cli.group('instances')
def instances():
    """Commands for instances"""

@instances.command('snapshot',
  help="Create snapshots of all volumes")
@click.option('--project', default=None, 
  help="Only instances for project (tag Project:<name>)")
def create_snapshots(project):
    "Snapshot EC2 Instance Volumes"
    instances = get_instances(project)
    for instance in instances:
        print("Stopping {0}...".format(instance.id))

        instance.stop()
        instance.wait_until_stopped()
        for volume in instance.volumes.all():
            print("Creating snapshot of {0}...".format(volume.id))
            volume.create_snapshot(Description="Created by shotty")
        
        print("Starting {0}...".format(instance.id))

        instance.start()
        instance.wait_until_running()
    print('Snapshots completed')
    return   

@instances.command('list')
@click.option('--project', default=None, 
  help="Only instances for project (tag Project:<name>)")
def list_instances(project):
    "List EC2 Instances"
    instances = get_instances(project)
    for instance in instances:
        tags = { tag['Key']: tag['Value'] for tag in instance.tags or [] }
        print(', '.join((
            instance.id,
            instance.instance_type,
            instance.placement['AvailabilityZone'],
            instance.state['Name'],
            instance.public_dns_name,
            tags.get('Project', '<no project>')
        )))

    return

@instances.command('stop')
@click.option('--project', default=None, 
  help="Only instances for project (tag Project:<name>)")
def stop_instances(project):
    "Stop EC2 instances"
    instances = get_instances(project)
    for instance in instances:
        print("Stopping {0}...".format(instance.id))
        try:
            instance.stop()
        except botocore.exceptions.ClientError as error:
            print("Could not stop {0}. ".format(instance.id) + str(error))
            continue

    return

@instances.command('start')
@click.option('--project', default=None, 
  help="Only instances for project (tag Project:<name>)")
def start_instances(project):
    "Start EC2 instances"
    instances = get_instances(project)
    for instance in instances:
        print("Starting {0}...".format(instance.id))
        try:
            instance.start()
        except botocore.exceptions.ClientError as error:
            print("Could not start {0}. ".format(instance.id) + str(error))
            continue

    return

@cli.group('volumes')
def volumes():
    """Commands for volumes"""

@volumes.command('list')
@click.option('--project', default=None, 
  help="Only volumes for project (tag Project:<name>)")
def list_volumes(project):
    "List EC2 Instance Volumes"
    instances = get_instances(project)
    for instance in instances:
        for volume in instance.volumes.all():
            print(', '.join((
                volume.id,
                instance.id,
                volume.state,
                str(volume.size) + 'GiB',
                volume.encrypted and "Encrypted" or "Not Encrypted"
            )))

    return

@cli.group('snapshots')
def snapshots():
    """Commands for snapshots"""

@snapshots.command('list')
@click.option('--project', default=None, 
  help="Only snapshots for project (tag Project:<name>)")
def list_snapshots(project):
    "List EC2 Instance Volume Snapshots"
    instances = get_instances(project)
    for instance in instances:
        for volume in instance.volumes.all():
            for snapshot in volume.snapshots.all():
                print(', '.join((
                    snapshot.id,
                    volume.id,
                    instance.id,
                    snapshot.state,
                    snapshot.progress,
                    snapshot.start_time.strftime("%c")
                )))

    return


if __name__ == '__main__':
    cli()