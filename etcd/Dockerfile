FROM gliderlabs/alpine:3.1

ENV ETCD_VERSION v0.4.6
ENV ETCD_DATA_DIR /etcddata
ENV ETCD_NAME etcd
ENV ETCDCTL_PEERS 10.1.42.1:4001

RUN apk-install wget ca-certificates \
  && wget --no-check-certificate -qO- https://github.com/coreos/etcd/releases/download/$ETCD_VERSION/etcd-$ETCD_VERSION-linux-amd64.tar.gz \
  | tar -z -x -f - \
  && mv /etcd-$ETCD_VERSION-linux-amd64/etcd /etcd-$ETCD_VERSION-linux-amd64/etcdctl /bin/ \
  && rm -rf /etcd-$ETCD_VERSION-linux-amd64 \
  && apk del wget ca-certificates

VOLUME ["/etcddata"]

EXPOSE 4001 7001

CMD ["/bin/etcd"]
