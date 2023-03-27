import boto3
import pandas as pd

# create a glue client
glue = boto3.client('glue')

# get a list of tables in the given database
database_name = 'dlx_ddm_consume'
response = glue.get_tables(DatabaseName=database_name)
table_list = response['TableList']

# find the life_events_ccpa table
table_name = 'life_events_ccpa'
table_exists = False
table_location = ''

for table in table_list:
    if table['Name'] == table_name:
        table_exists = True
        table_location = table['StorageDescriptor']['Location']

if not table_exists:
    print(f"Table {table_name} does not exist.")

# read the data from the table
s3 = boto3.client('s3')
object_key = table_location.replace('s3://', '').replace('/', '', 1)
bucket_name = object_key.split('/')[0]
s3_path = '/'.join(object_key.split('/')[1:])

response = s3.select_object_content(
    Bucket=bucket_name,
    Key=s3_path,
    ExpressionType='SQL',
    Expression="SELECT * FROM s3object s WHERE s.event_date > '2020-01-01'",
    InputSerialization={
        'CSV': {"FileHeaderInfo": "USE", "RecordDelimiter": "\n", "FieldDelimiter": ","},
        'CompressionType': 'NONE'
    },
    OutputSerialization={
        'CSV': {}
    }
)

# extract data from response
records = []
for event in response['Payload']:
    if 'Records' in event:
        records.append(event['Records']['Payload'].decode('utf-8'))

# convert data into a dataframe and save it as a csv file
df = pd.read_csv(pd.compat.StringIO(''.join(records)))
df.to_csv('life_events_ccpa_filtered.csv', index=False)