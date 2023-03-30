"""
In the `aws_s3_bucket_object` resource, instead of using `filemd5`,
we are using `${md5(file())}` to calculate the MD5 hash of the file.
This should update the `source_hash` when the file changes in the
`glue_files/site-packages/` directory.
"""

data "archive_file" "site_packages" {
  type        = "zip"
  source_dir  = "glue-files/site-packages/"
  output_path = "site-packages.zip"
}

resource "aws_s3_bucket_object" "glue_site_packages" {
  bucket = "your-bucket-name"
  key    = "glue-files/site-packages.zip"
  source = "${path.module}/${data.archive_file.site_packages.output_path}"
  etag = "${md5(file("${path.module}/glue-files/site-packages.zip"))}"
}