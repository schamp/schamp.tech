import os
import sys

import boto3
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

ACCESS_KEY=os.environ.get('AWS_ACCESS_KEY_ID')
SECRET=os.environ.get('AWS_SECRET_ACCESS_KEY')
BUCKET=os.environ.get('AWS_S3_BUCKET')
OUTPUT_DIR='output'

content_types = {
    '.css': 'text/css',
    '.html': 'text/html',
    '.js': 'text/javascript',
    '.json': 'application/json',
    '.map': 'application/json',
    '.txt': 'text/plain',
    '.xml': 'text/xml',
}

if ACCESS_KEY and SECRET and BUCKET:
    s3 = boto3.resource('s3', aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET)
    bucket = s3.Bucket(BUCKET)

    for root, dirs, files in os.walk(OUTPUT_DIR):
        for name in files:
            path = os.path.join(root, name)
            relative_path = os.path.relpath(path, OUTPUT_DIR)
            print("Uploading file: {}".format(relative_path))
            extra_args = {}
            for ext, t in content_types.items():
                if name.endswith(ext):
                    extra_args['ContentType'] = t
                    break

            bucket.upload_file(Key=relative_path, Filename=path, ExtraArgs=extra_args)
else:
    print("Must supply AWS_ACCESS_KEY_ID, AWS_SECRET_ACCES_KEY, and AWS_S3_BUCKET in environment!")
    sys.exit(1)
