FROM tensorflow/tensorflow:2.0.4-py3

# pip install
COPY requirements.txt /scripts/requirements.txt
RUN pip install -r /scripts/requirements.txt

ADD code /scripts/code
ADD train /scripts/train

# will be overwritten by kf pipeline
ENTRYPOINT [ "python3", "/scripts/code/run.py" ]
