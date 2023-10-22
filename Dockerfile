FROM python:3.11.0-slim
LABEL authors="xander"

ARG REQUIREMENTS_FILE

WORKDIR /app
EXPOSE 80
ENV PYTHONUNBUFFERED 1


#CMD ["sh", "/entrypoint-web.sh"]
#COPY ./docker/ /

COPY ./requirements/ ./requirements
RUN pip install -r ./requirements/${REQUIREMENTS_FILE}

COPY . ./