FROM tensorflow/tensorflow:2.0.4-py3

# pip install
COPY requirements.txt /scripts/requirements.txt
RUN pip install -r /scripts/requirements.txt

COPY fetch_from_source.py /scripts/fetch_from_source.py
COPY userinput.csv /scripts/userinput.csv

# will be overwritten by kf pipeline
ENTRYPOINT [ "python3", "/scripts/fetch_from_source.py" ]
