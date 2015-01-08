# Service Discovery Demo

## Service Registry

Registering our services in the key / value store. We use `progrium/registrator` for this.

Run registrator on each host:

```console
$ export DOCKER_HOST=tcp://172.17.8.101:2375
$ docker run -d -v /var/run/docker.sock:/tmp/docker.sock --net host --name registrator progrium/registrator -ttl 30 -ttl-refresh 20 etcd://10.1.42.1:4001/app/services
d271885144bda8fe91fdca3f1a6820bdea987282fcec350913234cb52c4203ed
$ export DOCKER_HOST=tcp://172.17.8.102:2375
$ docker run -d -v /var/run/docker.sock:/tmp/docker.sock --net host --name registrator progrium/registrator -ttl 30 -ttl-refresh 20 etcd://10.1.42.1:4001/app/services
7555d93c6660db9901e9e66c55eadaa946c667c9b1a116f23136674a63800f8e
$ export DOCKER_HOST=tcp://172.17.8.103:2375
$ docker run -d -v /var/run/docker.sock:/tmp/docker.sock --net host --name registrator progrium/registrator -ttl 30 -ttl-refresh 20 etcd://10.1.42.1:4001/app/services
bcb8c905bca0612e9848b37bd0a493fe5d55d8808daa88136757076e65fcaeb1
```

Verify we have no services registered:

```console
$ docker run -e ETCDCTL_PEERS="10.1.42.1:4001" andyshinn/etcd etcdctl ls
/coreos.com
```

The `/coreos.com` key is internal to CoreOS. It is used for update locking information.

Lets fire up Redis on `core02`:

```console
$ export DOCKER_HOST=tcp://172.17.8.102:2375
$ docker run -d --name redis -p 6379 redis
219eea5f97a490ca3bd6b33d5e8ca7ecbbc14ff05113a3660bc87d3be1c7a81c
```

Verify it has been added to the registry:

```console
$ docker run --rm -e ETCDCTL_PEERS="10.1.42.1:4001" andyshinn/etcd etcdctl ls
/coreos.com
/app
$ docker run --rm -e ETCDCTL_PEERS="10.1.42.1:4001" andyshinn/etcd etcdctl ls --recursive /app
/app/services
/app/services/redis
/app/services/redis/core02:redis:6379
$ docker run --rm -e ETCDCTL_PEERS="10.1.42.1:4001" andyshinn/etcd etcdctl get /app/services/redis/core02:redis:6379
172.17.8.102:49153
```

The newly added key at `/app/services/redis/core02:redis:6379` contains the location of our Redis instance at `172.17.8.102:49153`.

## Service Discovery

Discovering and using the services registered in our key / value store.

Run the webapp on `core01`:

```console
$ export DOCKER_HOST=tcp://172.17.8.101:2375
$ docker run -d --name webapp -p 5000 andyshinn/webapp
d36bdfbbab1513366d2db52361fd9a4e0a8de5a7f8f1b1fa444b31d94d9acb73
```

The webapp runs on port 5000. The automatically mapped port on the host will be registered in etcd. We can verify this:

```console
$ docker run --rm -e ETCDCTL_PEERS="10.1.42.1:4001" andyshinn/etcd etcdctl ls --recursive /app
/app/services
/app/services/webapp
/app/services/webapp/core01:webapp:5000
/app/services/redis
/app/services/redis/core02:redis:6379
$ docker run --rm -e ETCDCTL_PEERS="10.1.42.1:4001" andyshinn/etcd etcdctl get /app/services/webapp/core01:webapp:5000
172.17.8.101:49156
```

Cool! The application is available at the URL http://172.17.8.101:49156. But we generally don't hit our application directly. We want to go through a reverse proxy like nginx. Let's run it on `core03`:

```console
$ export DOCKER_HOST=tcp://172.17.8.103:2375
$ docker run -d --name router -p 80:80 andyshinn/router
5fbf91c2e9a32a844870d07563237620e7a0684da83d9a15329001611e0046bb
```

Now we should be able to visit http://172.17.8.101 to hit the application going through nginx. This router is special in that it will automatically discover application at the etcd `/app/services/webapp` key and add them to the upstream. Lets launch more on other hosts:

```console
$ export DOCKER_HOST=tcp://172.17.8.101:2375
$ docker run -d --name webapp -p 5000 andyshinn/webapp
1403b157d7e0eeaa6f6c2710067472b3a954105c9db7f529b6656bac59b5c6e0
$ export DOCKER_HOST=tcp://172.17.8.102:2375
$ docker run -d --name webapp -p 5000 andyshinn/webapp
$ 036bdc10c7757d13549940a0b7557310d182631e9339340f5b3f922c0f24a48f
```

Now by browsing to http://172.17.8.101 and refreshing multiple times, we can see the balancing happening among our webapp nodes.

# Canonical Commands

```
docker run -d -v /var/run/docker.sock:/tmp/docker.sock --net host --name registrator progrium/registrator -ttl 30 -ttl-refresh 20 etcd://10.1.42.1:4001/app/services

docker run andyshinn/etcd etcdctl ls

docker run -d --name redis -p 6379 redis

docker run andyshinn/etcd etcdctl ls --recursive /app

docker run -d --name webapp -p 5000 andyshinn/webapp

docker run -d --name router -p 80:80 andyshinn/router
```
