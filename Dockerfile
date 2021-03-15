FROM python:3.8.8-buster
WORKDIR /doris
ADD . /doris

# Install and deploy with uwsgi
RUN pip install -e .[deploy]

# Seed the data andrun the app
CMD sleep 10 ; python doris_add_test_entries.py ; uwsgi doris.ini
