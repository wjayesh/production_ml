import os
import boto3
import argparse
from pathlib2 import Path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='fetch data args')
    parser.add_argument('-b', '--base_path',
                        help='directory to base', default='/scripts/')
    parser.add_argument(
        '-m', '--model', help='directory to model', default='model')
    parser.add_argument(
        '-s', '--s3_bucket', help='bucket to store model to', default='model-bucket')

    args = parser.parse_args()

    model_path = Path(args.base_path).joinpath(
        args.model).resolve(strict=False)
    model_file = model_path.joinpath('model_latest.h5')

    print('Model file path: ', model_file)

    s3 = boto3.resource('s3', region_name='us-east-1',
                        aws_access_key_id='AKI...',
                        aws_secret_access_key='zte...')
    s3.Bucket(args.s3_bucket).upload_file(
        Filename=str(model_file), Key='model_latest.h5')
    print('Uploaded model to bucket')
