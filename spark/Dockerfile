FROM apache/spark:3.5.7-python3

USER root

# Set working directory
WORKDIR /opt/spark-apps

# Copy requirements file
COPY ./spark/requirements.txt /opt/requirements.txt

# Install Python packages
RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install -r /opt/requirements.txt

EXPOSE 1011
EXPOSE 2020

