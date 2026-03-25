from fastapi import FastAPI, APIRouter, HTTPException, Header
from fastapi.responses import StreamingResponse
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
import io
import csv
from pathlib import Path
from pydantic import BaseModel, Field, ConfigDict, EmailStr
from typing import List, Optional
import uuid
from datetime import datetime, timezone
import resend


ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Resend email setup
resend.api_key = os.environ.get("RESEND_API_KEY", "")
FROM_EMAIL = os.environ.get("FROM_EMAIL", "onboarding@lazygen.site")
ADMIN_KEY = os.environ.get("ADMIN_KEY", "")

# Create the main app without a prefix
app = FastAPI()

# Create a router with the /api prefix
api_router = APIRouter(prefix="/api")


# Define Models
class StatusCheck(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    client_name: str
    timestamp: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class StatusCheckCreate(BaseModel):
    client_name: str

# Waitlist Models
class WaitlistEntry(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    email: EmailStr
    phone: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class WaitlistCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=100)

class WaitlistResponse(BaseModel):
    success: bool
    message: str
    id: str = None


# ── helpers ──────────────────────────────────────────────────────────────────

def _send_confirmation_email(name: str, email: str) -> None:
    """Send a branded confirmation email via Resend. Fires-and-forgets (sync call, wrapped)."""
    if not resend.api_key:
        logger.warning("RESEND_API_KEY not set – skipping confirmation email")
        return

    html_body = f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>You're on the LazyGen Waitlist 🐼</title>
</head>
<body style="margin:0;padding:0;background:#FFFFFF;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif;">
  <div style="max-width:600px;margin:0 auto;padding:40px 20px;color:#0A0A0A;">
    <p style="font-size:24px;margin-bottom:24px;">🐼</p>
    <h1 style="font-size:24px;font-weight:700;margin:0 0 16px;letter-spacing:-0.5px;">Hey {name}, you're on the list!</h1>
    
    <p style="font-size:16px;line-height:1.6;margin:0 0 24px;">
      Thanks for joining the <strong>LazyGen waitlist</strong>. You've successfully locked in your spot for early access.
    </p>

    <div style="border-left:4px solid #0A0A0A;padding-left:20px;margin:24px 0;">
      <p style="font-size:14px;color:#666;margin:0 0 8px;text-transform:uppercase;letter-spacing:1px;">First 100 users get special perks</p>
      <p style="font-size:16px;margin:0;line-height:1.6;">
        We'll notify you as soon as we open the doors. LazyBot is getting ready to handle your job applications so you don't have to.
      </p>
    </div>

    <p style="font-size:15px;font-weight:600;margin:32px 0 12px;">What to expect from LazyBot:</p>
    <ul style="font-size:15px;line-height:1.8;margin:0;padding-left:20px;color:#444;">
      <li>Automated resume-to-job matching</li>
      <li>One-click applications that actually work</li>
      <li>Saving up to 200+ hours of manual hunting every month</li>
    </ul>

    <p style="font-size:14px;color:#888;margin:40px 0 0;font-style:italic;">
      Stay lazy,<br/>
      <strong>Team LazyBot 🐼</strong>
    </p>
    
    <hr style="border:none;border-top:1px solid #EEE;margin:40px 0 20px;" />
    <p style="font-size:12px;color:#AAA;text-align:center;">
      Questions? Reply to this email or hit us at support@lazygen.site
    </p>
  </div>
</body>
</html>
"""

    try:
        resend.Emails.send({
            "from": f"LazyBot 🐼 <{FROM_EMAIL}>",
            "to": [email],
            "subject": "you're on the LazyGen waitlist 🐼",
            "html": html_body,
        })
        logger.info(f"Confirmation email sent to {email}")
    except Exception as e:
        logger.error(f"Failed to send confirmation email to {email}: {e}")


def _require_admin(x_admin_key: Optional[str]) -> None:
    """Raise 403 if the provided admin key doesn't match."""
    if not ADMIN_KEY:
        raise HTTPException(status_code=500, detail="ADMIN_KEY not configured on server")
    if x_admin_key != ADMIN_KEY:
        raise HTTPException(status_code=403, detail="Forbidden — invalid admin key")


# ── routes ───────────────────────────────────────────────────────────────────

@api_router.get("/")
async def root():
    return {"message": "Hello World"}

@api_router.post("/status", response_model=StatusCheck)
async def create_status_check(input: StatusCheckCreate):
    status_dict = input.model_dump()
    status_obj = StatusCheck(**status_dict)

    doc = status_obj.model_dump()
    doc['timestamp'] = doc['timestamp'].isoformat()

    _ = await db.status_checks.insert_one(doc)
    return status_obj

@api_router.get("/status", response_model=List[StatusCheck])
async def get_status_checks():
    status_checks = await db.status_checks.find({}, {"_id": 0}).to_list(1000)

    for check in status_checks:
        if isinstance(check['timestamp'], str):
            check['timestamp'] = datetime.fromisoformat(check['timestamp'])

    return status_checks


# Waitlist endpoints

@api_router.post("/waitlist", response_model=WaitlistResponse)
async def join_waitlist(input: WaitlistCreate):
    # Check if email already exists
    existing = await db.waitlist.find_one({"email": input.email}, {"_id": 0})
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered for waitlist")

    waitlist_entry = WaitlistEntry(
        name=input.name,
        email=input.email,
        phone=input.phone
    )

    doc = waitlist_entry.model_dump()
    doc['created_at'] = doc['created_at'].isoformat()

    await db.waitlist.insert_one(doc)

    # Send confirmation email (non-blocking — failure doesn't break signup)
    _send_confirmation_email(input.name, input.email)

    return WaitlistResponse(
        success=True,
        message="Successfully joined the waitlist!",
        id=waitlist_entry.id
    )


@api_router.get("/waitlist/count")
async def get_waitlist_count():
    count = await db.waitlist.count_documents({})
    return {"count": count}


@api_router.get("/waitlist")
async def get_all_waitlist_entries(x_admin_key: Optional[str] = Header(default=None)):
    """Return all waitlist entries as JSON. Requires X-Admin-Key header."""
    _require_admin(x_admin_key)
    entries = await db.waitlist.find({}, {"_id": 0}).to_list(10000)
    return {"count": len(entries), "entries": entries}


@api_router.get("/waitlist/export")
async def export_waitlist_csv(x_admin_key: Optional[str] = Header(default=None)):
    """Download all waitlist entries as a CSV file. Requires X-Admin-Key header."""
    _require_admin(x_admin_key)
    entries = await db.waitlist.find({}, {"_id": 0}).to_list(10000)

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["id", "name", "email", "phone", "created_at"])
    writer.writeheader()
    for entry in entries:
        writer.writerow({
            "id": entry.get("id", ""),
            "name": entry.get("name", ""),
            "email": entry.get("email", ""),
            "phone": entry.get("phone", ""),
            "created_at": entry.get("created_at", ""),
        })

    output.seek(0)
    filename = f"lazygen_waitlist_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M%S')}.csv"
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'}
    )


# ── app setup ─────────────────────────────────────────────────────────────────

app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
