import os
from flask import Flask, request, jsonify

app = Flask(__name__)

APP_NAME = "student-ml-api"


def read_version():
    """Read the application version from the VERSION file.

    Falls back to the APP_VERSION env var (useful in containers) and
    finally to '0.0.0' if neither is available.
    """
    version_path = os.path.join(os.path.dirname(__file__), "VERSION")
    try:
        with open(version_path, "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return os.environ.get("APP_VERSION", "0.0.0")


APP_VERSION = read_version()
MODEL_VERSION = os.environ.get("MODEL_VERSION", "model-1")


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "application": APP_NAME,
        "version": APP_VERSION,
        "model_version": MODEL_VERSION
    }), 200


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True)

    if not data or "value" not in data:
        return jsonify({"error": "Missing 'value' field in request body"}), 400

    value = data["value"]

    if not isinstance(value, (int, float)) or isinstance(value, bool):
        return jsonify({"error": "'value' must be a number"}), 400

    prediction = value * 2  # simple placeholder "model"

    return jsonify({
        "input": value,
        "prediction": prediction
    }), 200


if __name__ == "__main__":
    # Bind to 0.0.0.0 (not 127.0.0.1) so the app is reachable
    # from outside the Docker container.
    app.run(host="0.0.0.0", port=5000)
