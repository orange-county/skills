---
name: ocfl
description: "Interact with Orange County, FL government services: property lookup, permits, inmate search, pet adoption, and form assistance."
---

# Orange County FL Skill

Interact with Orange County, Florida government services via CLI and natural language.

## Capabilities

1. **Property Lookup** — Parcel data, zoning, owner, value, permits
2. **Permit Info** — Requirements, fees, checklists for common permits
3. **Inmate Search** — Current inmates, booking lists, first appearances
4. **Pet Adoption** — Search adoptable animals with filters
5. **Form Wizard** — Generate filled PDFs for common permits

## Quick Commands

```bash
# Property lookup (with ArcGIS geocoding)
ocfl property "1321 Apopka Airport Rd, Apopka"
ocfl property 292234916802030

# Permit info
ocfl permit fence
ocfl permit pool
ocfl permit adu

# Inmate search
ocfl inmate "John Smith"
ocfl inmate --bookings

# Pet search (with live scraping)
ocfl pets --ready --limit 10
ocfl pets --type dog
```

## Features

### ✅ Working Now
- **Property Geocoding** — Uses Orange County ArcGIS to validate addresses (100% confidence scoring)
- **Pet Scraping** — Live data from Animal Services shelter (name, ID, location, adoption status)
- **Booking PDF Check** — Verifies daily inmate booking list availability
- **Permit Database** — Offline reference for fence, pool, roof, ADU, garage sale, tree permits

### 🔜 Coming Soon
- Direct parcel data from Property Appraiser API
- Inmate search scraping
- Telegram wizard integration

## Data Sources

### Property Appraiser (ocpafl.org)

**Parcel Search API:**
```bash
# Street view with parcel
curl "https://maps.ocpafl.org/streetview/?parcel=PARCEL_ID"

# Parcel data via ArcGIS
curl "https://services1.arcgis.com/OCGIS/arcgis/rest/services/Parcels/FeatureServer/0/query?where=PARCEL_ID='XXX'&outFields=*&f=json"
```

**Web Search (fallback):**
- URL: `https://ocpaweb.ocpafl.org/parcelsearch`
- Search by: Owner name, address, parcel ID

### GIS Data Hub (ArcGIS)

**Base URL:** `https://ocgis-datahub-ocfl.hub.arcgis.com`

**Available Layers:**
- Parcels
- Zoning
- Future Land Use
- Commission Districts
- Flood Zones
- School Zones

**API Pattern:**
```bash
# Query parcels by address
curl "https://services1.arcgis.com/XXXXX/arcgis/rest/services/Parcels/FeatureServer/0/query" \
  -d "where=SITUS_ADDR LIKE '%MAIN ST%'" \
  -d "outFields=*" \
  -d "f=json"
```

### Fast Track Permits (fasttrack.ocfl.net)

**Portal:** `https://fasttrack.ocfl.net/OnlineServices/`

**Permit Types Available Online:**
- Fence (residential) — $38 base fee
- Windows/Doors
- Roofing
- Pool/Spa
- AC changeout
- Tent permits
- Owner-builder permits

**Workflow:**
1. Create account (Contractor or Homeowner)
2. Upload required documents
3. Pay fees via credit card or escrow
4. Schedule inspections

### BestJail Inmate System

**Search URL:** `https://netapps.ocfl.net/BestJail/Home/Inmates`

**Daily Reports (PDF):**
- Bookings: `https://netapps.ocfl.net/BestJail/PDF/bookings.pdf`
- Population Stats: `https://netapps.ocfl.net/BestJail/PDF/ethnicity_values.pdf`
- First Appearances: `https://netapps.ocfl.net/BestJail/Home/FirstAppearance`

**Update Frequency:** Every 30 minutes

### Animal Services

**Adoptable Pets:** `http://www.orangecountyanimalservicesfl.net/Adopt/AnimalsinShelter.aspx`

**Filters:**
- Type: Cat, Dog
- Size: 25 lbs or less, Over 25 lbs
- Age: <1, 1-3, 4-6, 7-9, 10+
- Gender: Male, Female
- Status: Ready to Go Home, Not Adopted

**Pagination:** `?page=N&pagesize=12`

**Foster Pets:** `http://www.ocnetpets.com/GetInvolved/FosterCare.aspx`

## Common Permits Reference

### Fence Permit (Residential)

**Requirements:**
- Dimensioned site plan or survey with fence location
- Easement Acknowledgement Form (if in easement)
- PDF file named: `A100-Siteplan-Fence`

**Fees:** $38 + additional fees if code enforcement violation ($40)

**Review Time:** 4 business days

**Expiration:** 180 days from approval

**Height Limits:**
- Front yard: typically 4 feet
- Side/rear yard: typically 6 feet
- Check specific zoning district

**Submit via:** Fast Track Online

### Pool/Spa Permit

**Requirements:**
- Site plan with pool location, setbacks
- Barrier/fence plan (safety code)
- Equipment location
- Electrical permit (separate)

**Submit via:** Fast Track Online

### ADU (Accessory Dwelling Unit)

**Requirements:**
- Site plan
- Floor plan
- Elevations
- Impact fee calculations

**Recent Changes:** Vision 2050 updates (check current status)

## Form Templates

### Fence Permit Wizard

When user wants a fence permit, collect:

1. **Property Address** — verify it's in unincorporated Orange County
2. **Fence Location** — front, side, rear, or combination
3. **Fence Height** — 4ft front, 6ft side/rear typical
4. **Material** — wood, vinyl, aluminum, chain-link, other
5. **Is property in an easement?** — check survey or plat
6. **Owner or Contractor?** — determines Fast Track account type

Generate checklist:
```
☐ Site plan or survey with fence marked
☐ Easement form (if applicable)  
☐ Fast Track account created
☐ $38 fee ready
```

### Garage Sale Permit

**Requirements:**
- Address
- Date(s) of sale
- Max 3 sales per year

**Submit:** Email to zoning@ocfl.net

## Useful Contacts

| Department | Phone | Email |
|------------|-------|-------|
| Building Safety | 407-836-5550 | — |
| Zoning Division | 407-836-3111 | zoning@ocfl.net |
| Property Appraiser | 407-836-5044 | — |
| Tax Collector | 407-434-0312 | — |
| Animal Services | 407-836-3111 | — |
| Corrections (Inmates) | 407-836-3400 | — |
| GIS | 407-836-0066 | GIS@ocfl.net |
| Planning | — | Planning@ocfl.net |

## Scripting Notes

### Property Lookup Script

```python
#!/usr/bin/env python3
"""ocfl_property.py - Look up Orange County FL property data"""

import requests
import sys

ARCGIS_BASE = "https://services1.arcgis.com"
OCPA_SEARCH = "https://ocpaweb.ocpafl.org"

def search_by_address(address: str) -> dict:
    """Search parcel by street address"""
    # Use ArcGIS geocoding or OCPA search
    # Returns: parcel_id, owner, address, zoning, value, etc.
    pass

def get_parcel_details(parcel_id: str) -> dict:
    """Get full parcel details by ID"""
    # Query ArcGIS feature service
    # Returns: all parcel attributes
    pass

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: ocfl_property.py <address or parcel_id>")
        sys.exit(1)
    # Implementation here
```

### Inmate Search Script

```python
#!/usr/bin/env python3
"""ocfl_inmate.py - Search Orange County jail inmates"""

import requests
from bs4 import BeautifulSoup

BESTJAIL_URL = "https://netapps.ocfl.net/BestJail"
BOOKINGS_PDF = f"{BESTJAIL_URL}/PDF/bookings.pdf"

def search_inmate(name: str) -> list:
    """Search current inmates by name"""
    # Scrape BestJail search page
    # Returns: list of matching inmates with charges, bond, etc.
    pass

def get_daily_bookings() -> bytes:
    """Download today's booking list PDF"""
    response = requests.get(BOOKINGS_PDF)
    return response.content

if __name__ == "__main__":
    # Implementation here
    pass
```

### Pet Search Script

```python
#!/usr/bin/env python3
"""ocfl_pets.py - Search adoptable pets in Orange County"""

import requests
from bs4 import BeautifulSoup

SHELTER_URL = "http://www.orangecountyanimalservicesfl.net/Adopt/AnimalsinShelter.aspx"

def search_pets(
    pet_type: str = None,  # cat, dog
    size: str = None,       # small, large
    age_range: str = None,  # <1, 1-3, 4-6, 7-9, 10+
    gender: str = None,     # male, female
    ready_only: bool = False
) -> list:
    """Search adoptable pets with filters"""
    # Scrape shelter page with filters
    # Returns: list of pets with name, id, status, photo_url
    pass

if __name__ == "__main__":
    # Implementation here
    pass
```

## Caveats

1. **Jurisdiction Check** — Services only apply to unincorporated Orange County. Cities (Orlando, Winter Park, etc.) have their own systems.

2. **Fast Track Account Required** — Most permit submissions require a registered account.

3. **PDF Naming** — Fast Track is case-sensitive on file names. Must match exactly.

4. **Inmate Data Lag** — 30-minute update delay on BestJail.

5. **Vision 2050 Status** — Comprehensive plan currently in dispute with state. Check current zoning rules before relying on new standards.

## Future Enhancements

- [ ] Webhook for inmate status changes
- [ ] Pet adoption alerts via Telegram
- [ ] Automated permit status checking
- [ ] Meeting agenda keyword alerts
- [ ] Property value change notifications
- [ ] Integration with Tax Collector for payment status
