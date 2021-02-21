FROM ubuntu:bionic

# install required packages
RUN apt-get clean
RUN apt-get update \
    && apt-get install -y  git \
    net-tools \
    aptitude \
    build-essential \
    python3-setuptools \
    python3-dev \
    python3-pip \
    software-properties-common \
    ansible \
    curl \
    iptables \
    iputils-ping \
    sudo

ENV export LC_ALL=C.UTF-8
ENV export LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8
# install containernet (using its Ansible playbook)
COPY . /containernet
WORKDIR /containernet/ansible
RUN ansible-playbook -i "localhost," -c local --skip-tags "notindocker" install.yml
WORKDIR /containernet
RUN make develop

RUN pip3 install "more-itertools<=5.0.0"

# tell containernet that it runs in a container
ENV CONTAINERNET_NESTED 1
# Important: This entrypoint is required to start the OVS service
RUN service openvswitch-switch start
ENV CELERY_BROKER_URL redis://redis:6379/0
ENV CELERY_RESULT_BACKEND redis://redis:6379/0

RUN mkdir -p /usr/src/celery
WORKDIR /usr/src/celery
COPY requirements.txt /usr/src/celery
#dibuat manual lagi
#ovs-ctl show
RUN sudo /usr/share/openvswitch/scripts/ovs-ctl start
RUN pip3 install -r requirements.txt
COPY . /usr/src/celery
# production
EXPOSE 6633 6653 6640
ENTRYPOINT celery -A tasks worker -l INFO
