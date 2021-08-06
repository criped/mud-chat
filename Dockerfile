FROM python:3.9

RUN apt-get update
RUN apt-get install -y locales
RUN sed -i -e 's/# en_US.UTF-8 UTF-8/en_US.UTF-8 UTF-8/' /etc/locale.gen && \
    locale-gen
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

RUN pip3 install --upgrade pip

RUN mkdir /src
# COPY requirements and RUN pip install BEFORE adding the rest of your code, this will cause Docker's caching mechanism
# to prevent re-installing (all your) dependencies when you made a change a line or two in your app.
COPY /src/requirements/ /src/requirements/
RUN pip3 install -r /src/requirements/base.txt


COPY deployment/init.sh /usr/local/bin/
RUN chmod u+x /usr/local/bin/init.sh

# Copy source code
ADD /src/ /src/

WORKDIR /src

EXPOSE 80
ENTRYPOINT ["init.sh"]
