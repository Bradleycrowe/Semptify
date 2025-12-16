"""
Rent Calculator FastAPI Router - Rent calculation tools
Converted from Flask blueprint: rent_calculator_routes.py
"""
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import Dict, Any

from engines.rent_calculator_engine import rent_calculator_logic

router = APIRouter(tags=["rent-calculator"])
templates = Jinja2Templates(directory="templates")


class RentCalculatorRequest(BaseModel):
    data: Dict[str, Any]


@router.get("/rent_calculator", response_class=HTMLResponse)
async def rent_calculator_page(request: Request):
    """
    Rent calculator UI page
    
    Provides:
    - Rent affordability calculator
    - Rent increase analysis
    - Cost breakdown tools
    """
    return templates.TemplateResponse("rent_calculator.html", {"request": request})


@router.post("/api/rent_calculator")
async def rent_calculator_api(request: RentCalculatorRequest):
    """
    Rent calculator API endpoint
    
    Performs rent calculations based on provided data.
    """
    result = rent_calculator_logic(request.data)
    return result
