FROM tensorflow/tensorflow:2.0.4-py3

# pip install
COPY requirements.txt /scripts/requirements.txt
RUN pip install -r /scripts/requirements.txt

ADD export_to_s3.py /scripts/export_to_s3.py
ADD model /scripts/model

# will be overwritten by kf pipeline
ENTRYPOINT [ "python3", "/scripts/export_to_s3.py" ]
