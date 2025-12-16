"""
Rent Ledger FastAPI Router - Financial tracking for tenancy
Converted from Flask blueprint: ledger_routes.py
Coincides with calendar to document all monetary transactions
"""
from fastapi import APIRouter, Request, UploadFile, File, HTTPException, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Literal
from datetime import datetime
import json
import os

from calendar_vault_bridge import CalendarVaultBridge
from security import validate_user_token

router = APIRouter(prefix="/ledger", tags=["ledger"])
templates = Jinja2Templates(directory="templates")
bridge = CalendarVaultBridge()


# ============================================================================
# Pydantic Models
# ============================================================================

class TransactionRequest(BaseModel):
    user_token: str
    transaction_type: Literal['rent', 'deposit', 'fee', 'utility', 'late_fee', 'refund']
    amount: float
    date: str
    description: Optional[str] = ""
    payment_method: Optional[str] = ""


class TransactionResponse(BaseModel):
    ok: bool
    message: str
    transaction_id: str
    receipts: int


class TransactionListResponse(BaseModel):
    ok: bool
    transactions: List[Dict[str, Any]]
    total_paid: float
    total_refunded: float
    net_paid: float


class SummaryResponse(BaseModel):
    ok: bool
    summary: Dict[str, Dict[str, Any]]


# ============================================================================
# Routes
# ============================================================================

@router.get("", response_class=HTMLResponse)
async def ledger_view(request: Request):
    """Rent ledger interface - financial calendar"""
    return templates.TemplateResponse("ledger/ledger_view.html", {"request": request})


@router.post("/api/add-transaction", response_model=TransactionResponse)
async def add_transaction(
    transaction_type: str = Form(...),
    amount: float = Form(...),
    date: str = Form(...),
    user_token: str = Form(...),
    description: Optional[str] = Form(""),
    payment_method: Optional[str] = Form(""),
    files: Optional[List[UploadFile]] = File(None)
):
    """
    Add monetary transaction to ledger AND calendar
    
    Supports file uploads for receipts
    """
    # Validate user token
    if not user_token or not validate_user_token(user_token):
        raise HTTPException(status_code=401, detail="Invalid user token")

    # Create transaction record
    transaction = {
        'transaction_type': transaction_type,
        'amount': amount,
        'date': date,
        'description': description,
        'payment_method': payment_method,
        'timestamp': datetime.utcnow().isoformat()
    }

    # Save to ledger file
    ledger_file = os.path.join('uploads', 'vault', f'user_{user_token}_ledger.json')
    os.makedirs(os.path.dirname(ledger_file), exist_ok=True)

    ledger_entries = []
    if os.path.exists(ledger_file):
        with open(ledger_file, 'r', encoding='utf-8') as f:
            ledger_entries = json.load(f)

    transaction_id = f"txn_{datetime.utcnow().isoformat().replace(':', '').replace('-', '').replace('.', '')}"
    transaction['transaction_id'] = transaction_id

    ledger_entries.append(transaction)

    with open(ledger_file, 'w', encoding='utf-8') as f:
        json.dump(ledger_entries, f, indent=2)

    # Add to calendar as event
    event_data = {
        'title': f"{transaction['transaction_type'].replace('_', ' ').title()} - ${transaction['amount']}",
        'description': transaction['description'],
        'event_date': transaction['date'],
        'event_type': 'rent',
        'transaction_id': transaction_id
    }

    # Handle receipt uploads
    document_ids = []
    if files:
        for file in files:
            if file and file.filename:
                user_dir = os.path.join('uploads', 'vault', user_token)
                os.makedirs(user_dir, exist_ok=True)

                doc_id = f"receipt_{transaction_id}_{file.filename}"
                file_path = os.path.join(user_dir, doc_id)
                
                # Save uploaded file
                content = await file.read()
                with open(file_path, 'wb') as f:
                    f.write(content)

                # Create certificate
                import hashlib
                sha = hashlib.sha256(content).hexdigest()
                
                cert = {
                    'doc_id': doc_id,
                    'filename': file.filename,
                    'sha256': sha,
                    'timestamp': datetime.utcnow().isoformat(),
                    'uploaded_via': 'ledger',
                    'transaction_id': transaction_id,
                    'amount': transaction['amount']
                }

                cert_file = os.path.join(user_dir, f'{doc_id}.cert.json')
                with open(cert_file, 'w', encoding='utf-8') as f:
                    json.dump(cert, f, indent=2)

                document_ids.append(doc_id)

    # Catalog in calendar (optional)
    try:
        catalog_entry = bridge.catalog_event_with_documents(
            user_id=user_token,
            event_data=event_data,
            document_ids=document_ids
        )
    except Exception as e:
        print(f"[WARN] Calendar cataloging failed: {e}")

    return TransactionResponse(
        ok=True,
        message=f'Transaction recorded: {transaction_id}',
        transaction_id=transaction_id,
        receipts=len(document_ids)
    )


@router.get("/api/transactions", response_model=TransactionListResponse)
async def get_transactions(user_token: str):
    """Get all transactions for user with totals"""
    if not user_token or not validate_user_token(user_token):
        raise HTTPException(status_code=401, detail="Invalid user token")

    ledger_file = os.path.join('uploads', 'vault', f'user_{user_token}_ledger.json')

    if not os.path.exists(ledger_file):
        return TransactionListResponse(
            ok=True,
            transactions=[],
            total_paid=0,
            total_refunded=0,
            net_paid=0
        )

    with open(ledger_file, 'r', encoding='utf-8') as f:
        transactions = json.load(f)

    # Calculate totals
    total_paid = sum(
        t['amount'] for t in transactions
        if t['transaction_type'] in ['rent', 'deposit', 'fee', 'utility', 'late_fee']
    )
    total_refunded = sum(
        t['amount'] for t in transactions
        if t['transaction_type'] == 'refund'
    )

    return TransactionListResponse(
        ok=True,
        transactions=sorted(transactions, key=lambda x: x['date'], reverse=True),
        total_paid=total_paid,
        total_refunded=total_refunded,
        net_paid=total_paid - total_refunded
    )


@router.get("/api/summary", response_model=SummaryResponse)
async def get_summary(user_token: str):
    """Get financial summary grouped by month"""
    if not user_token or not validate_user_token(user_token):
        raise HTTPException(status_code=401, detail="Invalid user token")

    ledger_file = os.path.join('uploads', 'vault', f'user_{user_token}_ledger.json')

    if not os.path.exists(ledger_file):
        return SummaryResponse(ok=True, summary={})

    with open(ledger_file, 'r', encoding='utf-8') as f:
        transactions = json.load(f)

    # Group by month
    summary = {}
    for txn in transactions:
        month = txn['date'][:7]  # YYYY-MM
        if month not in summary:
            summary[month] = {'rent': 0, 'fees': 0, 'total': 0, 'count': 0}

        if txn['transaction_type'] == 'rent':
            summary[month]['rent'] += txn['amount']
        else:
            summary[month]['fees'] += txn['amount']

        summary[month]['total'] += txn['amount']
        summary[month]['count'] += 1

    return SummaryResponse(ok=True, summary=summary)
