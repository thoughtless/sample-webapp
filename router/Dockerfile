FROM gliderlabs/alpine:3.1

ENV CONFD_VERSION 0.7.1
ENV CONFD_INTERVAL 20
ENV CONFD_NODE 10.1.42.1:4001
ENV CONFD_BACKEND etcd

RUN apk-install bash wget ca-certificates nginx \
  && wget -qO /usr/local/bin/confd https://github.com/kelseyhightower/confd/releases/download/v$CONFD_VERSION/confd-$CONFD_VERSION-linux-amd64 \
  && apk del wget

COPY confd /etc/confd
COPY codep /usr/local/bin/codep
COPY nginx.conf /etc/nginx/nginx.conf

RUN chmod +x /usr/local/bin/confd /usr/local/bin/codep \
  && mkdir /etc/nginx/cache

EXPOSE 80

CMD codep \
  "nginx" \
  "confd -verbose -interval $CONFD_INTERVAL -node $CONFD_NODE"
