
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from awsglue.context import GlueContext
from pyspark.context import SparkContext
from pyspark.sql.functions import *
from pyspark.sql.types import StructType, StructField, StringType

# Get GLUE parameters
args = getResolvedOptions(sys.argv, ['JOB_NAME', 's3_input_path'])

# Create a Spark context
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session

# Define the schema for each layout
layout1_schema = StructType([StructField('col1', StringType()), StructField('col2', StringType())])
layout2_schema = StructType([StructField('col1', StringType()), StructField('col3', StringType())])
layout3_schema = StructType([StructField('col1', StringType()), StructField('col2', StringType()), StructField('col3', StringType())])

# Define the attributes for each layout
layout1_widths = [5, 10]
layout2_widths = [5, 15]
layout3_widths = [5, 10, 5]

# Read in the fixed width file using a custom input format with the width settings for each layout
dynamic_frame = glueContext.create_dynamic_frame.from_options(
    connection_type='s3',
    connection_options={'paths': [args['s3_input_path']]},
    format='fixed-width',
    format_options={
        'widths': ','.join(map(str, layout1_widths + layout2_widths + layout3_widths)),
        'skipHeader': 'false',
        'fillRecord': 'true',
        'recordDelimiter': '\n'
    }
)

# Split the dynamic frame into three separate dynamic frames based on the record length
dynamic_frame1 = dynamic_frame.filter(f'length(record) = {sum(layout1_widths)}')
dynamic_frame2 = dynamic_frame.filter(f'length(record) = {sum(layout2_widths)}')
dynamic_frame3 = dynamic_frame.filter(f'length(record) = {sum(layout3_widths)}')

# Convert each dynamic frame to a data frame with the appropriate schema
data_frame1 = dynamic_frame1.toDF(layout1_schema)
data_frame2 = dynamic_frame2.toDF(layout2_schema)
data_frame3 = dynamic_frame3.toDF(layout3_schema)

# Show the data frames
data_frame1.show()
data_frame2.show()
data_frame3.show()