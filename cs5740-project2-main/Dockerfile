FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    bash \
    build-essential \
    vim \
    nano \
    curl \
    software-properties-common \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip3 install -r requirements.txt

# Set the default command to run bash
CMD ["bash"]
