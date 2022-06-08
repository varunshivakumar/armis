# use specific version, use secure base image
FROM python:latest 
LABEL Maintainer="varunshivakumar"

WORKDIR /home

# user non-root user
# RUN groupadd -r collectoruser && useradd -r -g collectoruser collectoruser
# USER collectoruser

COPY collector.py config.ini requirements.txt ./

# verify dependencies
RUN pip install -r requirements.txt

CMD [ "python", "./collector.py"]