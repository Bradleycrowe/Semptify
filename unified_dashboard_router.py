"""
Unified Dashboard Router - Single GUI with 5 role-based access levels
admin > manager > advocate > attorney > user
"""
from fastapi import APIRouter, Request, Query, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Optional
from pydantic import BaseModel
from role_guards import get_user_role, has_role_access, get_accessible_features, ROLE_HIERARCHY

router = APIRouter(tags=["unified-dashboard"])
templates = Jinja2Templates(directory="templates")

@router.get("/", response_class=HTMLResponse)
async def root(request: Request, user_token: Optional[str] = Query(None)):
    if not user_token:
        return templates.TemplateResponse("token_entry.html", {"request": request})
    return RedirectResponse(url=f"/dashboard?user_token={user_token}")

@router.get("/dashboard", response_class=HTMLResponse)
async def unified_dashboard(request: Request, user_token: Optional[str] = Query(None)):
    if not user_token:
        return RedirectResponse(url="/")
    role = get_user_role(user_token)
    if not role:
        raise HTTPException(status_code=401, detail="Invalid token")
    features = get_accessible_features(role)
    return templates.TemplateResponse("unified_dashboard.html", {
        "request": request, "user_token": user_token, "role": role,
        "role_level": ROLE_HIERARCHY[role], "features": features
    })

@router.get("/api/dashboard/role")
async def get_role_info(user_token: Optional[str] = Query(None)):
    if not user_token:
        raise HTTPException(status_code=401, detail="Token required")
    role = get_user_role(user_token)
    if not role:
        raise HTTPException(status_code=401, detail="Invalid token")
    return {"role": role, "level": ROLE_HIERARCHY[role], "features": get_accessible_features(role)}
