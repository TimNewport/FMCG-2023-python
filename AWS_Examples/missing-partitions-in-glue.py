import boto3

def lambda_handler(event, context):
    # Retrieve database and table name from event parameter
    database_name = event['database_name']
    table_name = event['table_name']

    # Initialize Glue and S3 clients
    glue = boto3.client('glue')
    s3 = boto3.client('s3')

    # Get table details from Glue
    table_details = glue.get_table(DatabaseName=database_name, Name=table_name)

    # Get S3 location of the table
    s3_location = table_details['Table']['StorageDescriptor']['Location']

    # Parse S3 bucket and key from S3 location
    s3_bucket = s3_location.split('/')[2]
    s3_key = '/'.join(s3_location.split('/')[3:])

    # Retrieve existing partitions from S3
    existing_partitions = set()
    for obj in s3.list_objects(Bucket=s3_bucket, Prefix=s3_key)['Contents']:
        if '/' in obj['Key'][len(s3_key)+1:]:
            partition_str = obj['Key'][len(s3_key)+1:].split('/')[0]
            existing_partitions.add(partition_str)

    # Parse partition keys from Glue
    partition_keys = table_details['Table']['PartitionKeys']
    partition_key_str = ','.join([partition_key['Name'] for partition_key in partition_keys])

    # Check for missing partitions
    for partition_combination in [(p1,) for p1 in existing_partitions] + [(p1, p2) for p1 in existing_partitions for p2 in existing_partitions]:
        if partition_combination not in [partition['Values'] for partition in table_details['Table']['PartitionKeys']]:
            partition_value_str = ','.join(["'{}'".format(partition_value) for partition_value in partition_combination])
            print("ALTER TABLE {}.{} ADD IF NOT EXISTS PARTITION ({}) LOCATION '{}'".format(database_name, table_name, partition_key_str, s3_location+"/"+'/'.join(partition_combination)))
