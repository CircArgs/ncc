FROM python:3
WORKDIR /inc

# Setup base image deps
RUN apt-get update && apt-get install -y \
  python3 \
  build-essential \
  gcc-multilib \
  libncurses5-dev \
  libx11-dev \
  uuid-dev \
  wget \
  && rm -rf /var/lib/apt/lists/*

COPY . /ncc
RUN pip install -e /ncc && rm -rf /ncc

ENTRYPOINT ["/ncc/tests/test_compiler.sh"]

