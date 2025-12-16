# Justice-Grade API Pack - Integration Guide

## 🏛️ Overview

The **Justice-Grade API Pack** provides comprehensive tenant empowerment through 8 API categories with 20+ endpoints. Every API call includes learning observations for adaptive improvement.

**Core Mission**: Give tenants the same data access that landlords and property managers have, plus legal research tools that level the playing field.

---

## 📊 API Categories

### 1. Legal & Civic APIs
- **CourtListener** - Search eviction cases, tenant rights precedents, landlord litigation history
- **GovInfo** - Federal and state statutes, housing regulations, eviction law

### 2. Landlord & Property Ownership APIs  
- **RentCast** - Property owner lookup, rental history, ownership chains
- **County Assessor** - Property values, tax records, sale history
- **Landlord Litigation** - Track serial evictors, habitability violators

### 3. Document Intelligence APIs
- **Azure Document Intelligence** - AI-powered lease/notice extraction
- **Google Vision API** - OCR for images and scanned documents
- **Local PyMuPDF + pytesseract** - Free fallback option

### 4. Multilingual & Accessibility APIs
- **LibreTranslate** - Free, self-hostable translation (EN/ES/SO/HMN)
- **DeepL** - Premium translation (best quality)
- **Microsoft Translator** - Azure-backed translation
- **OpenAI Whisper** - Speech-to-text for accessibility

### 5. Finance & Data APIs
- **Yahoo Finance** - Stock market data, wage trend analysis
- **CoinGecko** - Cryptocurrency prices
- **ExchangeRate.host** - Currency conversion for international tenants

### 6. Housing & Community APIs
- **OpenStreetMap** - Map rental properties, eviction hotspots, tenant resources, legal aid offices

### 7. Utility APIs
- **OpenWeatherMap** - Weather data for habitability cases
- **REST Countries** - Country info for international tenant support

### 8. Fun & Resonance APIs
- **The Cat API** - Stress relief content
- **Dog CEO API** - Dog images/facts
- **JokeAPI** - Jokes for building rapport
- **NASA APOD** - Astronomy pictures for perspective

---

## 🚀 Quick Start

### 1. Install Dependencies

```powershell
# Navigate to project directory
cd C:\Semptify\Semptify

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install required packages
pip install requests aiohttp yfinance
```

### 2. Configure API Keys

Create or edit `.env` file:

```bash
# Legal APIs
COURT_LISTENER_API_KEY=your_key_here
GOVINFO_API_KEY=your_key_here

# Landlord Lookup
RENTCAST_API_KEY=your_key_here

# Document Intelligence
AZURE_DOCUMENT_INTELLIGENCE_KEY=your_key_here
AZURE_DOCUMENT_INTELLIGENCE_ENDPOINT=https://your-resource.cognitiveservices.azure.com/
GOOGLE_VISION_API_KEY=your_key_here

# Multilingual
LIBRETRANSLATE_URL=https://libretranslate.com  # Or self-hosted
LIBRETRANSLATE_API_KEY=optional
DEEPL_API_KEY=your_key_here
DEEPL_FREE_TIER=true
AZURE_TRANSLATOR_KEY=your_key_here
OPENAI_API_KEY=your_key_here  # For Whisper

# Utility
OPENWEATHER_API_KEY=your_key_here
NASA_API_KEY=your_key_here  # Or use DEMO_KEY

# Optional Fun APIs
CAT_API_KEY=your_key_here
COINGECKO_API_KEY=your_key_here  # Pro tier only
```

### 3. Start Server

```powershell
# Start FastAPI server
python -m uvicorn semptify_app:app --host 127.0.0.1 --port 8000 --reload
```

### 4. Check API Status

```powershell
# View configured APIs
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/status" | ConvertTo-Json -Depth 5
```

---

## 🔑 API Key Setup Instructions

### Free Tier APIs (No Credit Card Required)

#### CourtListener
1. Visit: https://www.courtlistener.com/sign-in/register/
2. Register free account
3. Go to: https://www.courtlistener.com/api/rest-info/
4. Copy API token
5. Add to `.env`: `COURT_LISTENER_API_KEY=your_token`
6. **Rate Limit**: 5,000 calls/day free tier

#### LibreTranslate (Self-Hosted Option)
1. **Option A** - Use public instance: `LIBRETRANSLATE_URL=https://libretranslate.com`
2. **Option B** - Self-host with Docker:
   ```powershell
   docker run -ti --rm -p 5000:5000 libretranslate/libretranslate
   ```
   Then set: `LIBRETRANSLATE_URL=http://localhost:5000`
3. **No API key required** for basic usage

#### NASA Open APIs
1. Visit: https://api.nasa.gov/
2. Register for free key (instant approval)
3. Add to `.env`: `NASA_API_KEY=your_key`
4. **Rate Limit**: 1,000 calls/hour

#### OpenWeatherMap
1. Visit: https://home.openweathermap.org/users/sign_up
2. Verify email and get API key
3. Add to `.env`: `OPENWEATHER_API_KEY=your_key`
4. **Rate Limit**: 1,000 calls/day free tier

### Premium APIs (Require Payment Info)

#### RentCast
1. Visit: https://app.rentcast.io/app/signup
2. Free trial available, then $49-$99/month
3. **Critical for**: property owner lookup, landlord case tracking
4. **Rate Limit**: 500 calls/day on Starter plan

#### DeepL
1. Visit: https://www.deepl.com/pro-api
2. Free tier: 500,000 characters/month
3. Add to `.env`: `DEEPL_API_KEY=your_key`
4. **Best quality** translations for legal documents

#### Azure Document Intelligence
1. Create Azure account: https://azure.microsoft.com/free/
2. $200 free credit for 30 days
3. Create "Document Intelligence" resource
4. Copy key and endpoint to `.env`
5. **Rate Limit**: 15 calls/minute free tier

#### OpenAI Whisper
1. Visit: https://platform.openai.com/signup
2. Add payment method ($5 minimum)
3. Get API key: https://platform.openai.com/api-keys
4. **Pricing**: ~$0.006 per minute of audio

### No Key Required (Always Free)

- Yahoo Finance (via yfinance library)
- CoinGecko (50 calls/minute free)
- ExchangeRate.host
- OpenStreetMap Nominatim
- REST Countries
- Dog CEO API
- JokeAPI

---

## 📖 API Usage Examples

### Legal Case Search

```powershell
# Search eviction cases in Minnesota
$result = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/legal/cases?query=eviction&jurisdiction=minnesota&limit=10"
$result | ConvertTo-Json
```

**Response Schema**:
```json
{
  "source": "CourtListener/GovInfo",
  "query": "eviction",
  "jurisdiction": "minnesota",
  "count": 10,
  "cases": [
    {
      "case_name": "Tenant v. Landlord",
      "court": "Minnesota District Court",
      "date_filed": "2024-03-15",
      "docket_number": "27-CV-24-1234",
      "summary": "Eviction case - tenant raised retaliation defense",
      "outcome": "Dismissed - landlord failed to prove just cause",
      "citation": "Minn. Stat. § 504B.285",
      "relevance_score": 0.95
    }
  ]
}
```

### Landlord Lookup

```powershell
# Find property owner
$address = "123 Main St, Minneapolis, MN 55401"
$result = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/landlord/lookup?address=$address"
```

**Response Schema**:
```json
{
  "source": "RentCast/County Assessor",
  "address": "123 Main St, Minneapolis, MN 55401",
  "owner": {
    "name": "ABC Property Management LLC",
    "mailing_address": "456 Corporate Blvd, Suite 200",
    "phone": "(612) 555-0123",
    "email": "contact@abcpm.com",
    "company": "ABC Property Management LLC",
    "llc_registration": "MN-123456789"
  },
  "property": {
    "parcel_id": "12-345-678-90",
    "assessed_value": 250000,
    "year_built": 1985,
    "square_feet": 1200,
    "bedrooms": 2,
    "bathrooms": 1
  },
  "rental_history": {
    "previous_owners": ["XYZ Rentals (2015-2020)", "John Smith (2005-2015)"],
    "sale_history": [
      {"date": "2020-06-15", "price": 235000, "buyer": "ABC Property Management LLC"}
    ],
    "rent_estimates": {
      "current": 1400,
      "market_average": 1350,
      "percentile": 65
    }
  }
}
```

### Landlord Litigation History

```powershell
# Find landlord's court cases
$result = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/landlord/cases?landlord_name=ABC Property Management&state=MN"
```

**Response Schema**:
```json
{
  "landlord": "ABC Property Management LLC",
  "state": "MN",
  "cases": [
    {
      "case_number": "27-CV-23-5678",
      "date_filed": "2023-08-20",
      "case_type": "Eviction",
      "outcome": "Dismissed - failed to meet notice requirements",
      "tenant_represented": true
    }
  ],
  "statistics": {
    "total_eviction_filings": 47,
    "evictions_dismissed": 12,
    "habitability_violations": 3,
    "retaliation_findings": 2,
    "license_violations": 1
  }
}
```

### Translation (Multilingual Support)

```powershell
# Translate to Spanish
$body = @{
    text = "You have the right to remain in your home during the appeal process."
    target_lang = "es"
    source_lang = "en"
} | ConvertTo-Json

$result = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/translate" -Method GET -Body $body -ContentType "application/json"
```

**Response Schema**:
```json
{
  "source": "LibreTranslate/DeepL",
  "source_lang": "en",
  "target_lang": "es",
  "original": "You have the right to remain...",
  "translation": "Tiene el derecho de permanecer en su hogar durante el proceso de apelación.",
  "confidence": 0.98
}
```

**Supported Languages**:
- `en` - English
- `es` - Spanish
- `so` - Somali
- `hmn` - Hmong
- Plus 100+ others via DeepL/LibreTranslate

### Document Analysis

```powershell
# Upload and analyze lease document
$file = Get-Item "lease_agreement.pdf"
$form = @{
    file = $file
    doc_type = "lease"
    use_ai = "true"
}
$result = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/document/analyze" -Method POST -Form $form
```

**Response Schema**:
```json
{
  "source": "Azure Document Intelligence",
  "filename": "lease_agreement.pdf",
  "doc_type": "lease",
  "extracted_fields": {
    "landlord": "ABC Property Management LLC",
    "tenant": "Jane Doe",
    "property_address": "123 Main St, Apt 2B, Minneapolis, MN",
    "rent_amount": 1400.00,
    "lease_start": "2024-01-01",
    "lease_end": "2024-12-31",
    "security_deposit": 1400.00,
    "signatures": [
      {"party": "landlord", "signed": true, "date": "2023-12-20"},
      {"party": "tenant", "signed": true, "date": "2023-12-22"}
    ]
  },
  "confidence_scores": {
    "landlord": 0.99,
    "tenant": 0.98,
    "rent_amount": 0.95
  }
}
```

### Housing Map Data

```powershell
# Find tenant resources near location
$result = Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/housing/map?location=Minneapolis,MN&radius_miles=5"
```

**Response Schema**:
```json
{
  "location": "Minneapolis, MN",
  "radius_miles": 5,
  "center_coords": {"lat": 44.9778, "lon": -93.2650},
  "housing_data": {
    "rental_properties": [
      {"name": "Riverside Apartments", "lat": 44.9725, "lon": -93.2419, "units": 50}
    ],
    "affordable_housing": [
      {"name": "Section 8 Housing Authority", "lat": 44.9656, "lon": -93.2712}
    ],
    "tenant_unions": [
      {"name": "Twin Cities Tenants Union", "address": "...", "phone": "..."}
    ],
    "legal_aid_offices": [
      {"name": "Mid-Minnesota Legal Aid", "address": "...", "phone": "..."}
    ],
    "courts": [
      {"name": "Hennepin County District Court", "address": "...", "phone": "..."}
    ]
  }
}
```

---

## ⚡ Rate Limits & Best Practices

### Rate Limits by Provider

| Provider | Free Tier | Rate Limit | Notes |
|----------|-----------|------------|-------|
| CourtListener | 5,000/day | 50/min | Generous free tier |
| RentCast | 500/day | 10/min | Starter plan ($49/mo) |
| LibreTranslate | Unlimited* | 20/min | *Self-hosted option |
| DeepL | 500k chars/mo | Varies | Free tier available |
| OpenWeatherMap | 1,000/day | 60/min | Free tier |
| NASA | 1,000/hour | 30/min | DEMO_KEY available |
| OpenStreetMap | Unlimited* | 1/sec | *Usage policy applies |

### Best Practices

1. **Cache Results**: Store frequently accessed data (statutes, property records)
2. **Batch Requests**: Group related queries when possible
3. **Respect Rate Limits**: Use `api_config.py` rate limit checking
4. **Implement Fallbacks**: Use fallback providers (DeepL → LibreTranslate)
5. **Monitor Usage**: Check `/api/status` endpoint regularly
6. **Local Alternatives**: Use yfinance, pytesseract for offline capability

---

## 🔧 Troubleshooting

### Common Issues

#### "API integration pending" messages
**Cause**: API key not configured  
**Fix**: Add required key to `.env` file and restart server

#### Rate limit errors
**Cause**: Too many requests  
**Fix**: Implement caching or upgrade to paid tier

#### Translation quality issues
**Cause**: Using LibreTranslate free tier  
**Fix**: Upgrade to DeepL for legal document quality

#### Document extraction failures
**Cause**: Image quality or OCR limitations  
**Fix**: Use Azure Document Intelligence for AI-powered extraction

### Debug Mode

Enable detailed API logging:

```python
# In semptify_app.py startup
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## 🎯 Integration Roadmap

### Phase 1: Core Justice APIs (Current)
- ✅ Legal case search
- ✅ Landlord lookup
- ✅ Document intelligence
- ✅ Multilingual support

### Phase 2: Active API Integration (Next 2 Weeks)
- [ ] Connect CourtListener API
- [ ] Connect RentCast API
- [ ] Connect LibreTranslate
- [ ] Connect OpenWeatherMap
- [ ] Connect NASA APOD

### Phase 3: Premium Features (Month 2)
- [ ] Azure Document Intelligence integration
- [ ] DeepL translation for legal docs
- [ ] OpenAI Whisper for court testimony transcription
- [ ] Advanced landlord litigation tracking

### Phase 4: Advanced Analytics (Month 3)
- [ ] Eviction pattern analysis
- [ ] Rent vs. wage trend dashboards
- [ ] Landlord reputation scoring
- [ ] Predictive eviction risk modeling

---

## 📚 Additional Resources

### API Documentation Links

- **CourtListener**: https://www.courtlistener.com/api/rest-info/
- **RentCast**: https://developers.rentcast.io/reference/getting-started
- **LibreTranslate**: https://libretranslate.com/docs/
- **DeepL**: https://www.deepl.com/docs-api
- **Azure Document Intelligence**: https://learn.microsoft.com/azure/ai-services/document-intelligence/
- **OpenAI Whisper**: https://platform.openai.com/docs/guides/speech-to-text

### Semptify-Specific Guides

- `BLUEPRINT.md` - Overall architecture
- `document_intelligence.py` - Local document processing
- `learning_engine/` - Adaptive learning system
- `COMPLAINT_FILING_COMPLETE.md` - Legal document generation

---

## 🤝 Contributing

To add a new API provider:

1. Add configuration to `api_config.py`
2. Create endpoint in `justice_grade_api_routes.py`
3. Add learning observations
4. Update this README with usage examples
5. Test with real API keys

---

## 📞 Support

- **Issues**: File on GitHub repo
- **Questions**: Contact Brad (bradley@semptify.org)
- **API Key Issues**: Check provider documentation first

---

**Last Updated**: 2025-11-27  
**Version**: 1.0.0  
**Status**: API scaffolding complete, integration in progress
