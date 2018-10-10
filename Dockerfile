FROM debian:stretch-slim

# ensure local python is preferred over distribution python
ENV PATH /usr/local/bin:$PATH
ENV PYTHONUNBUFFERED 1

# http://bugs.python.org/issue19846
# > At the moment, setting "LANG=C" on a Linux system *fundamentally breaks Python 3*, and that's not OK.
ENV LANG C.UTF-8

# Installing OS Dependencies
RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends \
	libsqlite3-dev unixodbc-dev build-essential libssl-dev libffi-dev python3 python3-pip python3-dev python3-wheel apt-transport-https gnupg curl && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -rf /var/lib/apt/lists/* && \
	apt-get clean all

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
#RUN pip install --upgrade setuptools --user root

COPY requirements.txt .
COPY requirements-opt.txt .

#RUN pip3 install -r ./requirements.txt
#RUN pip3 install -r ./requirements-opt.txt
RUN LIBRARY_PATH=/lib:/usr/lib /bin/sh -c "pip3 install -r ./requirements.txt"
RUN LIBRARY_PATH=/lib:/usr/lib /bin/sh -c "pip3 install -r ./requirements-opt.txt"

RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/9/prod.list > /etc/apt/sources.list.d/mssql-release.list
RUN apt-get update && apt-get upgrade -y && ACCEPT_EULA=Y apt-get install -y --no-install-recommends msodbcsql17 \
    && rm -rf /var/lib/apt/lists/* \
	&& apt-get clean all

# Django service
EXPOSE 8000

#CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
CMD /bin/bash
