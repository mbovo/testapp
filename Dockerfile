FROM python:3.7.2-alpine3.7 as builder

RUN \
  mkdir -p /tmp/wheels && \
  apk add alpine-sdk musl-dev python3-dev libffi-dev openssl-dev

WORKDIR /tmp
COPY . .

RUN pip install -e .
RUN pip freeze | grep -v testapp > /tmp/wheels/requirements.txt && \
  pip wheel -r /tmp/wheels/requirements.txt --wheel-dir=/tmp/wheels --no-cache-dir
RUN python3 setup.py sdist bdist_wheel && \
  mv dist/*.whl /tmp/wheels


FROM python:3.7.2-alpine3.7
LABEL maintainer="manuel.bovo@gmail.com"
WORKDIR /usr/src/app
EXPOSE 5000
ENV TESTAPP_PORT="5000" \
  TESTAPP_LOG_LEVEL="info" \
  TESTAPP_STOP_TIMEOUT="2"
#COPY . .
COPY --from=builder /tmp/wheels/* /tmp/

RUN apk add git libstdc++ openssl libffi && \
  pip install --no-index --no-cache-dir --find-links=/tmp testapp && \
  rm -rf /tmp/*.whl && \
  rm -rf ~/.cache/pip

CMD [ "testapp" ]