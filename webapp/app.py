import os, socket, redis, etcd
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello():
    try:
        client = etcd.Client(host=os.environ.get('ETCD_HOST', '172.17.42.1'))
        key = client.read('/app/services/redis').value
        redis_url = client.get(key).value
        count = redis.StrictRedis.from_url("redis://{0}/0").format(redis_url).incr("counter")
    except:
        count = "redis not found"
    return "\n".join([
        '<div style="text-align: center; font-size: 128px;">Hello Docker Austin!</div>',
        '<div style="text-align: center; font-size: 64px;">Count: {0}</div>'.format(count),
        '<div style="text-align: center; font-size: 64px;">{0}</div>\n'.format(socket.gethostname())
    ])

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
