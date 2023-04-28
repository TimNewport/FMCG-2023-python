To write data out from Spark and PGP encrypt it using Secrets Manager in AWS Glue 3.0, follow these steps:

1. Set up and configure your AWS Glue job. Include the following in your job script:

```python
import boto3
import pgpy

# Initialize your AWS Secrets Manager client
secrets_manager_client = boto3.client('secretsmanager')

# Retrieve your PGP encryption key from Secrets Manager
pgp_key_secret = secrets_manager_client.get_secret_value(SecretId='<your-secret-id>')
pgp_key = pgpy.PGPKey.from_blob(pgp_key_secret['SecretString'].encode('utf-8'))

# Use PGP encryption to encrypt your data
encrypted_data = pgp_key.encrypt(data_to_encrypt)
```

2. Use Spark to read and process your data:

```python
from pyspark.sql import SparkSession

# Initialize your SparkSession
spark = SparkSession\
    .builder\
    .appName("my-glue-job")\
    .getOrCreate()

# Read your source data into a DataFrame
source_data = spark.read\
    .format("csv")\
    .option("header", "true")\
    .load("s3://my-bucket/my-source-data.csv")

# Process your data
processed_data = source_data.select("col1", "col2", "col3")

# Convert your DataFrame to a string
data_to_encrypt = processed_data.rdd.map(lambda x: ",".join(x)).collect()

# Use PGP encryption to encrypt your data
encrypted_data = pgp_key.encrypt(data_to_encrypt)

# Write your encrypted data to your target location
target_location = "s3://my-bucket/my-target-location"
encrypted_data.saveAsTextFile(target_location)
```

3. Finally, execute your Glue job to write out your data to your target location:

```python
# Execute your Glue job
glueContext.write_dynamic_frame.from_options(
    frame = DynamicFrame.fromDF(processed_data, glueContext, "processed_data"),
    connection_type = "s3",
    connection_options = {"path": target_location},
    format = "csv",
    format_options = {"header": "true"})
```