# Dockerfile for CI build
FROM python:3.8.1-alpine3.11

RUN mkdir /code
WORKDIR /code

# Copy source code to install python package
COPY setup.py /code/
COPY bt/ /code/bt/

# Install the python package
RUN python setup.py install

# Run tests on installed python package (using different directory)
RUN mkdir /bt_testing
WORKDIR /bt_testing
COPY models/ /bt_testing/models
COPY tests/ /bt_testing/tests
COPY setup.cfg requirements-test.txt /bt_testing/
RUN pip install -r requirements-test.txt

CMD "pytest"
