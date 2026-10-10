from flask import Flask, jsonify

app = Flask(__name__)

@app.get("/")
def home():
    return jsonify(
        project="Cloud Build CI/CD Pipeline with Approval Gates",
        message="Application is running",
        status="ok",
        approval_gate="Production release requires an authorized human approval"
    )

@app.get("/health")
def health():
    return jsonify(status="healthy"), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=False)
