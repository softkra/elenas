FROM python:3.9

ENV PYTHONUNBUFFERED=1
ENV C_FORCE_ROOT=1
ENV DJANGODIR=/django

RUN mkdir $DJANGODIR
WORKDIR $DJANGODIR

COPY requirements.txt $DJANGODIR/
RUN pip3 install -r requirements.txt
#RUN chown -R $USER:$GROUP ~/.npm
#RUN chown -R $USER:$GROUP ~/.config

COPY . $DJANGODIR/

RUN apt-get update && apt-get install -y gettext 