FROM python:3.11-alpine

ENV USR_LOCAL_BIN=/usr/local/bin  \
    PROJECT_ROOT=/application

ENV PYTHONPATH=$PYTHONPATH:$PROJECT_ROOT

ENV RUNTIME_PACKAGES="\
    libev \
    pcre \
    zlib-dev \
    libressl-dev \
    libffi-dev"

ENV BUILD_PACKAGES="\
    libev-dev \
    build-base \
    pcre-dev \
    gcc \
    build-base \
    linux-headers"

RUN apk update && \
    apk upgrade && \
    pip install --upgrade pip && \
    apk --no-cache add --virtual build-deps $BUILD_PACKAGES && \
    apk --no-cache add $RUNTIME_PACKAGES && \
    mkdir -p $PROJECT_ROOT/media_files/buffer_files

COPY ../requirements.txt $PROJECT_ROOT/

WORKDIR $PROJECT_ROOT

RUN pip install --no-cache-dir setuptools && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del build-deps && \
    rm -rf /var/cache/apk/* && \
    rm -rf /var/lib/apt/lists/*

COPY ./deploy/entrypoint.sh $USR_LOCAL_BIN/
COPY ./deploy/start_uvicorn.sh $USR_LOCAL_BIN/

RUN sed -i 's/\r//' $USR_LOCAL_BIN/*.sh \
    && chmod +x $USR_LOCAL_BIN/*.sh

ADD .. $PROJECT_ROOT
EXPOSE 8000
ENTRYPOINT ["entrypoint.sh"]
CMD ["start_uvicorn.sh"]