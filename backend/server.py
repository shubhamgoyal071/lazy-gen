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
    phone: str = Field(None, max_length=20)

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
<body style="margin:0;padding:0;background:#FAFAFA;font-family:'Segoe UI',Helvetica,Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="padding:40px 0;">
    <tr>
      <td align="center">
        <table width="580" cellpadding="0" cellspacing="0" style="background:#fff;border-radius:16px;overflow:hidden;border:1px solid #E5E5E5;">

          <!-- Header -->
          <tr>
            <td style="background:#0A0A0A;padding:36px 40px;text-align:center;">
              <p style="margin:0;font-size:32px;">🐼</p>
              <h1 style="margin:12px 0 0;color:#FAFAFA;font-size:28px;font-weight:900;letter-spacing:-1px;">LazyBot</h1>
              <p style="margin:6px 0 0;color:#888;font-size:12px;letter-spacing:3px;text-transform:uppercase;font-family:'Courier New',monospace;">apply smarter. not harder.</p>
            </td>
          </tr>

          <!-- Body -->
          <tr>
            <td style="padding:40px;">
              <p style="margin:0 0 8px;color:#0A0A0A;font-size:22px;font-weight:800;">hey {name} 👋</p>
              <p style="margin:0 0 24px;color:#444;font-size:15px;line-height:1.7;">
                you're officially on the <strong>LazyGen waitlist</strong>.<br/>
                no cap — you just made the smartest lazy decision of your life.
              </p>

              <div style="background:#0A0A0A;border-radius:12px;padding:24px;margin:24px 0;text-align:center;">
                <p style="margin:0 0 6px;color:#888;font-size:11px;font-family:'Courier New',monospace;text-transform:uppercase;letter-spacing:2px;">your spot is locked ✅</p>
                <p style="margin:0;color:#FAFAFA;font-size:15px;line-height:1.6;">
                  We'll hit you up the moment early access opens.<br/>
                  First <strong>100 users</strong> get special perks 🎁
                </p>
              </div>

              <p style="margin:24px 0 8px;color:#0A0A0A;font-size:14px;font-weight:700;">what lazybot does for you:</p>
              <ul style="margin:0;padding-left:20px;color:#555;font-size:14px;line-height:2;">
                <li>🧠 AI reads your resume like a recruiter</li>
                <li>⚡ matches you with jobs that actually fit</li>
                <li>🤖 applies on your behalf — literally</li>
                <li>😴 saves you 200+ hours every month</li>
              </ul>

              <p style="margin:32px 0 0;color:#888;font-size:13px;font-family:'Courier New',monospace;">
                stay lazy,<br/>
                <strong style="color:#0A0A0A;">team lazybot 🐼</strong>
              </p>
            </td>
          </tr>

          <!-- Footer -->
          <tr>
            <td style="background:#F5F5F5;padding:20px 40px;text-align:center;border-top:1px solid #E5E5E5;">
              <p style="margin:0;color:#AAA;font-size:11px;font-family:'Courier New',monospace;">
                questions? hit us at <a href="mailto:support@lazygen.site" style="color:#666;text-decoration:none;">support@lazygen.site</a>
              </p>
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>
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
