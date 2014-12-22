FROM ubuntu-debootstrap:trusty

ENV CONFD_VERSION 0.6.3
ENV CONFD_INTERVAL 30
ENV CONFD_NODE 172.17.42.1:4001
ENV CONFD_BACKEND etcd

RUN apt-get update -q \
  && DEBIAN_FRONTEND=noninteractive apt-get install -y -q wget nginx \
  && wget -qO /usr/local/bin/confd https://github.com/kelseyhightower/confd/releases/download/v$CONFD_VERSION/confd-$CONFD_VERSION-linux-amd64 \
  && apt-get remove -y wget \
  && apt-get autoremove -y \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists

ADD confd /etc/confd
ADD codep /usr/local/bin/codep
ADD nginx.conf /etc/nginx/nginx.conf

RUN chmod +x /usr/local/bin/confd /usr/local/bin/codep
RUN mkdir /etc/nginx/cache

EXPOSE 80

CMD codep \
  "nginx" \
  "confd -verbose -interval $CONFD_INTERVAL -node $CONFD_NODE"
