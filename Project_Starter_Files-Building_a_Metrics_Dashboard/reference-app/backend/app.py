from flask import Flask, render_template, request, jsonify
from flask_cors import CORS

import pymongo
from flask_pymongo import PyMongo
from flask_opentracing import FlaskTracing
from jaeger_client import Config
from jaeger_client.metrics.prometheus import PrometheusMetricsFactory
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from prometheus_flask_exporter import PrometheusMetrics
import logging
from prometheus_flask_exporter.multiprocess import GunicornInternalPrometheusMetrics

app = Flask(__name__)

app.config["MONGO_DBNAME"] = "example-mongodb"
app.config[
    "MONGO_URI"
] = "mongodb://example-mongodb-svc.default.svc.cluster.local:27017/example-mongodb"

mongo = PyMongo(app)

FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()
CORS(app)
#metrics = PrometheusMetrics(app)
metrics = GunicornInternalPrometheusMetrics(app, group_by='endpoint')
# static information as metric
metrics.info("backend_info", "Backend info", version="1.0.0")

logging.getLogger("").handlers = []
logging.basicConfig(format="%(message)s", level=logging.DEBUG)
logger = logging.getLogger(__name__)

def init_tracer(service):

    config = Config(
        config={
            "sampler": {"type": "const", "param": 1},
            "logging": True,
            "reporter_batch_size": 1,
        },
        service_name=service,
        validate=True
        #metrics_factory=PrometheusMetricsFactory(service_name_label=service),
    )

    # this call also sets opentracing.tracer
    return config.initialize_tracer()


tracer = init_tracer("backend")
flask_tracer = FlaskTracing(tracer, True, app)

# register extra metrics
metrics.register_default(
    metrics.counter(
        'path_counter', 'Request count by request path', labels={'path': lambda: request.path}
    )
)

# custom metric to be applied to multiple endpoints
endpoint_counter = metrics.counter(
    'endpoint_counter', 'Request count by endpoint',
    labels={'endpoint': lambda: request.endpoint}
)

@app.route("/")
@endpoint_counter
def homepage():
    with tracer.start_active_span('homepage'):
        resp = "Hello World"
        return jsonify(resp)


@app.route("/api")
@endpoint_counter
def my_api():
    with tracer.start_span('api'):
        answer = "something"
        return jsonify(repsonse=answer)


@app.route("/star", methods=["POST"])
@endpoint_counter
def add_star():
    with tracer.start_span('addstar'):
        star = mongo.db.stars
        name = request.json['name']
        distance = request.json['distance']
        star_id = star.insert({'name': name, 'distance': distance})
        new_star = star.find_one({'_id': star_id})
        output = {'name': new_star['name'], 'distance': new_star['distance']}
        return jsonify({'result': output})
    # star = mongo.db.stars
    # output = {}
    # payload = request.get_json()
    # with tracer.start_span("adding star") as span:
    #     try:            
    #         logger.info("Received: %s", payload)
    #         span.log_kv({"event" : "received input", "payload": payload})
    #         name = payload["name"]
    #         span.set_tag("name", name)
    #         distance = payload["distance"]
    #         star_id = star.insert({"name": name, "distance": distance})
    #         new_star = star.find_one({"_id": star_id})
    #         output = {"name": new_star["name"], "distance": new_star["distance"]}
    #         span.set_tag("http.status_code", "200")
    #         span.set_tag("name", name)
    #     except Exception:
    #         logger.error("Unable to process request %s", payload)
    #         span.set_tag("http.status_code", "500")
    #         span.set_tag("name", name)
    # return jsonify({"result": output})

class ExceptionUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.errorhandler(ExceptionUsage)
def handle_exception(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route("/403")
def status_code_403():
    status_code = 403
    raise ExceptionUsage("status_code: {}".format(status_code), status_code=status_code)


@app.route("/404")
def status_code_404():
    status_code = 404
    raise ExceptionUsage("status_code: {}".format(status_code), status_code=status_code)


@app.route("/500")
def status_code_500():
    status_code = 500
    raise ExceptionUsage("status_code: {}".format(status_code), status_code=status_code)


@app.route("/503")
def status_code_503():
    status_code = 503
    raise ExceptionUsage("status_code: {}".format(status_code), status_code=status_code)

if __name__ == "__main__":
    app.run()
