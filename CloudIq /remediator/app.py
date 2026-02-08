# app.py
import os
import json
import joblib
import logging
import subprocess
from typing import Any, Dict
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO)
app = FastAPI(title="CloudIQ Remediator")

MODEL_PATH = "/app/model.pkl"

# Load model once
model = None
if os.path.exists(MODEL_PATH):
    try:
        model = joblib.load(MODEL_PATH)
        logging.info("Loaded model from %s", MODEL_PATH)
    except Exception as e:
        logging.exception("Failed to load model: %s", e)
        model = None
else:
    logging.warning("No model found at %s — will use threshold fallback", MODEL_PATH)

# Simple expected payload schema (but we accept more)
class AlertPayload(BaseModel):
    status: str = None
    alerts: list = None
    # optional extra fields

def parse_cpu_from_payload(data: Dict[str, Any]) -> float:
    """
    Try to extract CPU% from common payload shapes:
    - CloudWatch via SNS (JSON inside 'Message')
    - Prometheus Alertmanager (alerts[].annotations.description)
    - Custom: alerts[].annotations.cpu
    Returns CPU percent (0.0 if not found).
    """
    # 1) If cloudwatch SNS -> message
    if 'Message' in data:
        try:
            msg = json.loads(data['Message'])
            # CloudWatch alarm messages vary; check common places
            if 'NewStateValue' in msg and 'Trigger' in msg:
                # not precise CPU value in default msg — return large value so remediate
                return 90.0
        except Exception:
            pass

    # 2) Prometheus-style: alerts[].annotations.description includes "CPU 92%"
    try:
        alerts = data.get("alerts") or data.get("Alerts") or []
        for a in alerts:
            ann = a.get("annotations", {})
            desc = ann.get("description", "") or ann.get("summary", "")
            if desc:
                import re
                m = re.search(r"(\d{1,3})\s*%|\bCPU[:\s]+(\d{1,3})", desc)
                if m:
                    for g in m.groups():
                        if g:
                            return float(g)
    except Exception:
        pass

    # 3) direct field e.g., data["cpu"]
    try:
        if "cpu" in data:
            return float(data["cpu"])
    except Exception:
        pass

    return 0.0

def scale_frontend(replicas: int = 3) -> Dict[str, str]:
    """Scale the front-end deployment in sock-shop"""
    try:
        subprocess.check_output(
            ["kubectl", "scale", "deploy", "front-end", "-n", "sock-shop", f"--replicas={replicas}"],
            stderr=subprocess.STDOUT
        )
        return {"status": "scaled", "replicas": str(replicas)}
    except subprocess.CalledProcessError as e:
        logging.exception("kubectl scale failed: %s", e.output.decode() if e.output else e)
        raise

@app.get("/")
async def root():
    return {"message": "🤖 CloudIQ Remediator v2 running!"}

@app.post("/remediate")
async def remediate(req: Request):
    try:
        payload = await req.json()
    except Exception:
        # If body not JSON, try form or text
        text = (await req.body()).decode(errors="ignore")
        try:
            payload = json.loads(text)
        except Exception:
            payload = {}

    logging.info("Received remediate payload: %s", payload)

    cpu_val = parse_cpu_from_payload(payload)
    logging.info("Parsed CPU value: %s", cpu_val)

    # If model exists, prepare features — adapt to your trained model's features
    if model is not None:
        try:
            # NOTE: adjust 'features' to match model training order/shape
            # Example assuming model expects [cpu, memory, disk_io, network_io]
            features = []
            features.append(cpu_val)
            features.append(float(payload.get("memory", 0)))
            features.append(float(payload.get("disk_io", 0)))
            features.append(float(payload.get("network_io", 0)))
            pred = model.predict([features])[0]
            logging.info("Model prediction: %s", pred)
            # assume model outputs 1 => anomaly / need remediation
            if int(pred) == 1 or cpu_val > 85:
                res = scale_frontend(replicas=3)
                return {"status": "success", "action": res, "cpu": cpu_val}
            else:
                return {"status": "ok", "reason": "model said normal", "cpu": cpu_val}
        except Exception as e:
            logging.exception("Model predict failed: %s", e)
            # fallback to threshold
            if cpu_val > 85:
                res = scale_frontend(replicas=3)
                return {"status": "success", "action": res, "cpu": cpu_val}
            return {"status": "failed", "error": str(e)}
    else:
        # No model: threshold fallback
        if cpu_val > 85:
            res = scale_frontend(replicas=3)
            return {"status": "success", "action": res, "cpu": cpu_val}
        return {"status": "ok", "cpu": cpu_val}

