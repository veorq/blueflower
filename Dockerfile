ARG UBUNTU_VERSION=16.04
FROM ubuntu:$UBUNTU_VERSION

ARG PYTHON_VERSION=2.7.9

# Install dependencies
RUN apt-get update \
  && apt-get install -y git wget gcc make openssl libssl-dev \
  && apt-get clean
  #&& apt-get install -y unzip libffi-dev libgdbm-dev libsqlite3-dev zlib1g-dev \
  #&& apt-get clean

# Build Python from source
WORKDIR /tmp/
RUN wget https://www.python.org/ftp/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tgz \
  && tar --extract -f Python-$PYTHON_VERSION.tgz \
  && cd ./Python-$PYTHON_VERSION/ \
  && ./configure --with-ensurepip=install --enable-optimizations --prefix=/usr/local \
  && make && make install \
  && cd ../ \
  && rm -r ./Python-$PYTHON_VERSION*

# check
RUN python --version \
  && pip --version

# Build scapy from source
#WORKDIR /tmp/
#RUN wget --trust-server-names https://github.com/secdev/scapy/archive/master.zip \
#  && unzip master \
#  && cd ./scapy-master \
#  && python setup.py install \
#  && cd ../ \
#  && rm -r master scapy-master

# install requirements
RUN pip install xlrd
RUN pip install pathlib 
RUN pip install pdfminer.six==20191110

# clone into blueflower
WORKDIR /app
RUN git clone https://github.com/veorq/blueflower.git
WORKDIR /app/blueflower
