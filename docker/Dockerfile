# Base image
FROM python:3.12.5-slim

# Install core OS dependencies
# - gcc: for psypcopg2-binary
# - git: for pre-commit
RUN apt-get update && \
    apt-get upgrade -y gcc vim

# Set app working directory
WORKDIR /usr/src/project

# Copy project files
COPY . .

# Install python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements/requirements.txt
CMD ["uvicorn", "main:app", "--use-colors","--access-log", "--reload", "--host", "0.0.0.0", "--port", "8001"]

