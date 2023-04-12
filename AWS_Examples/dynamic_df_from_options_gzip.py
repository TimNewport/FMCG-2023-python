Yes, `glueContext.create_dynamic_frame.from_options` has a connection option for GPG files. Here's an example code snippet that shows how to use this option:

```
from awsglue.context import GlueContext

glueContext = GlueContext(SparkContext.getOrCreate())

# Connection options for GPG files
connection_options = {
    "fileFormat": "csv",
    "compression": "gzip",
    "gpgKey": "s3://my-bucket/gpg/my-key.gpg"
}

# Creating dynamic frame from GPG file
dynamic_frame = glueContext.create_dynamic_frame.from_options(
                                    connection_type="s3",
                                    connection_options=connection_options,
                                    format="csv",
                                    format_options={"delimiter": ","},
                                    transformation_ctx="my_dynamic_frame")
```

In this code snippet, `connection_options` specify the file format, compression type, and the GPG key location for the input data file. You can replace the `gpgKey` value with the location of your own GPG key file. The `create_dynamic_frame.from_options` method then creates a dynamic frame using these connection options.