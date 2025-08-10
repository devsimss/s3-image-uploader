
import os, re, uuid
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import boto3
from botocore.config import Config
from dotenv import load_dotenv

# .env dosyasını okumak, yerel geliştirmeyi rahatlatır.
load_dotenv()

REGION = os.getenv("AWS_REGION", "eu-central-1")
BUCKET = os.getenv("S3_BUCKET", "")
ORIGIN = os.getenv("FRONTEND_ORIGIN", "http://localhost:5500")
ALLOWED_MIME = os.getenv("ALLOWED_MIME", r"^image/(jpeg|png|webp|gif)$")
KEY_PREFIX = os.getenv("KEY_PREFIX", "uploads/")
EXPIRES = int(os.getenv("EXPIRES", "300"))

if not BUCKET:
    raise RuntimeError("S3_BUCKET is not set")

app = FastAPI(title="S3 Uploader")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[ORIGIN],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

s3 = boto3.client("s3", region_name=REGION, config=Config(signature_version="s3v4"))

class Req(BaseModel):
    filename: str = Field(min_length=1)
    content_type: str = Field(min_length=1)

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/presign")
def presign(req: Req):
    # İçerik tipini kabaca kontrol ediyoruz.
    if not re.match(ALLOWED_MIME, req.content_type):
        raise HTTPException(400, "unsupported content type")

    safe = req.filename.replace("/", "_").replace("\\", "_")
    key = f"{KEY_PREFIX}{uuid.uuid4()}-{safe}"

    try:
        url = s3.generate_presigned_url(
            ClientMethod="put_object",
            Params={
                "Bucket": BUCKET,
                "Key": key,
                "ContentType": req.content_type,
                "ACL": "public-read",  # demo
            },
            ExpiresIn=EXPIRES,
        )
    except Exception as e:
        raise HTTPException(500, f"presign failed: {e}")

    public_url = f"https://{BUCKET}.s3.{REGION}.amazonaws.com/{key}"
    return {"url": url, "key": key, "headers": {"Content-Type": req.content_type}, "public_url": public_url}
