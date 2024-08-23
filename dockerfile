FROM ubuntu:latest

# add wget, git, and nginx
RUN apt update && apt install wget git nginx -y

# set up miniconda
ENV PATH="/opt/miniconda3/bin:${PATH}"
ARG PATH="/opt/miniconda3/bin:${PATH}"
RUN mkdir -p /opt/miniconda3 &&  \
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-aarch64.sh -O /opt/miniconda3/miniconda.sh && \
    bash /opt/miniconda3/miniconda.sh -b -u -p /opt/miniconda3 && \
    rm -rf /opt/miniconda3/miniconda.sh

# set up diet app for development
ENV FLASK_APP=/opt/diet/app/app.py
RUN cd opt/ && \
    git clone https://github.com/spkelle2/diet.git && \
    cd diet && \
    conda env create -f environment.yml && \
    . /opt/miniconda3/bin/activate && \
    conda activate diet && \
    pip install -e .

## set up nginx
RUN cp /opt/diet/app/sites-available/app /etc/nginx/sites-available && \
    ln -s /etc/nginx/sites-available/app /etc/nginx/sites-enabled

# run diet app with gunicorn as the server and nginx reverse proxy
ENTRYPOINT nginx && \
    . /opt/miniconda3/bin/activate && \
    conda activate diet && \
    cd /opt/diet/app/ && \
    gunicorn -w 4 -b 0.0.0.0:8000 app:app
