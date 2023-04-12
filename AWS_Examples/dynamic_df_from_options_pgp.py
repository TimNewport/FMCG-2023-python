Yes, `create_dynamic_frame.from_options` has a `connection_options` parameter to specify additional options for the data source. Here's an example of how to use it for PGP-encrypted files:

```python
from awsglue.context import GlueContext

# create Glue context
glueContext = GlueContext(sc)

# define connection options for PGP file
pgp_options = {
    "PGP_SECRET_KEY": "s3://path/to/secret_key",  # location of PGP secret key file
    "PGP_PUBLIC_KEY": "s3://path/to/public_key",  # location of PGP public key file
    "PGP_PASSPHRASE": "my_passphrase"            # passphrase for PGP key
}

# create dynamic frame using PGP connection options
dynamic_frame = glueContext.create_dynamic_frame.from_options(
    connection_type="s3",
    connection_options={
        "paths": ["s3://my-bucket/my-file.pgp"],
        "encryption": "pgp",
        "pgp": pgp_options
    },
)
```

Note: you'll need to replace `"s3://path/to/secret_key"` and `"s3://path/to/public_key"` with the actual S3 locations of your PGP key files. Also replace `"my_passphrase"` with the actual passphrase for your PGP key.