import os, socket, redis, etcd
from flask import Flask

app = Flask(__name__)
client = etcd.Client(host=os.environ.get('ETCD_HOST', '10.1.42.1'))

@app.route("/")
def hello():
    try:
        key = str(client.read('/app/services/redis')._children[0]['value'])
        redis_url = 'redis://{0}/0'.format(key)
        count = redis.StrictRedis.from_url(redis_url).incr("counter")
    except:
        count = "redis not found"
    return "\n".join([
        '<div style="text-align: center; font-size: 128px;">{0}</div>'.format(os.environ.get('WEBAPP_TITLE', 'Hello world... let\'s count!')),
        '<div style="text-align: center; font-size: 64px;">Count: {0}</div>'.format(count),
        '<div style="text-align: center; font-size: 64px;">Container ID: {0}</div>\n'.format(socket.gethostname())
    ])

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
