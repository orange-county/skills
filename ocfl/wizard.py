#!/usr/bin/env python3
"""
OCFL Telegram Wizard - Interactive guide for Orange County FL services

This module provides conversation flows for Clawdbot's Telegram interface.
It uses inline buttons to guide users through common tasks.
"""

import json
import subprocess
import sys
from typing import Optional

# Wizard state machine
FLOWS = {
    "main": {
        "text": "🍊 **Orange County FL Services**\n\nWhat would you like to do?",
        "buttons": [
            [{"text": "🏠 Property Lookup", "callback_data": "ocfl:property"}],
            [{"text": "🐕 Find a Pet", "callback_data": "ocfl:pets"}],
            [{"text": "📋 Permit Info", "callback_data": "ocfl:permit"}],
            [{"text": "👮 Inmate Search", "callback_data": "ocfl:inmate"}],
        ]
    },
    
    # Property flow
    "property": {
        "text": "🏠 **Property Lookup**\n\nI can look up property info by address or parcel ID.\n\n_Send me an address or parcel number, or tap below:_",
        "buttons": [
            [{"text": "📍 Use My Address", "callback_data": "ocfl:property:my_address"}],
            [{"text": "🔢 I Have a Parcel ID", "callback_data": "ocfl:property:parcel_prompt"}],
            [{"text": "« Back", "callback_data": "ocfl:main"}],
        ],
        "expects_input": True,
        "input_handler": "property_lookup"
    },
    
    # Pets flow
    "pets": {
        "text": "🐕 **Pet Adoption**\n\nOrange County Animal Services has pets ready for adoption!\n\nWhat are you looking for?",
        "buttons": [
            [
                {"text": "🐕 Dogs", "callback_data": "ocfl:pets:dog"},
                {"text": "🐈 Cats", "callback_data": "ocfl:pets:cat"},
            ],
            [{"text": "✅ Ready to Adopt Now", "callback_data": "ocfl:pets:ready"}],
            [{"text": "📊 Shelter Stats", "callback_data": "ocfl:pets:stats"}],
            [{"text": "« Back", "callback_data": "ocfl:main"}],
        ]
    },
    
    # Permit flow
    "permit": {
        "text": "📋 **Permit Information**\n\nSelect a permit type for requirements and fees:",
        "buttons": [
            [
                {"text": "🏗️ Fence", "callback_data": "ocfl:permit:fence"},
                {"text": "🏊 Pool", "callback_data": "ocfl:permit:pool"},
            ],
            [
                {"text": "🏠 Roof", "callback_data": "ocfl:permit:roof"},
                {"text": "🏘️ ADU", "callback_data": "ocfl:permit:adu"},
            ],
            [
                {"text": "🛒 Garage Sale", "callback_data": "ocfl:permit:garage_sale"},
                {"text": "🌳 Tree Removal", "callback_data": "ocfl:permit:tree"},
            ],
            [{"text": "« Back", "callback_data": "ocfl:main"}],
        ]
    },
    
    # Inmate flow
    "inmate": {
        "text": "👮 **Inmate Search**\n\nSearch current inmates or view today's bookings.\n\n_Send a name to search, or tap below:_",
        "buttons": [
            [{"text": "📋 Today's Bookings (PDF)", "callback_data": "ocfl:inmate:bookings"}],
            [{"text": "⚖️ First Appearances", "callback_data": "ocfl:inmate:appearances"}],
            [{"text": "« Back", "callback_data": "ocfl:main"}],
        ],
        "expects_input": True,
        "input_handler": "inmate_search"
    },
}


def run_ocfl(*args) -> dict:
    """Run the ocfl CLI and return parsed JSON output"""
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(script_dir, "scripts", "ocfl")
    
    try:
        result = subprocess.run(
            ["uv", "run", "--with", "requests", "--with", "beautifulsoup4", 
             "python", script_path] + list(args),
            capture_output=True,
            text=True,
            timeout=30,
            cwd=script_dir
        )
        if result.returncode == 0:
            return json.loads(result.stdout)
        else:
            return {"error": result.stderr or "Command failed"}
    except Exception as e:
        return {"error": str(e)}


def format_property_result(data: dict) -> str:
    """Format property lookup result for Telegram"""
    lines = ["🏠 **Property Lookup Result**\n"]
    
    if data.get("geocoding", {}).get("success"):
        lines.append(f"✅ **Address:** {data.get('matched_address')}")
        lines.append(f"📊 **Confidence:** {data.get('confidence')}%")
        lines.append("")
        
        if data.get("links"):
            lines.append("**Quick Links:**")
            if "property_search" in data["links"]:
                lines.append(f"• [Property Search]({data['links']['property_search']})")
            if "gis_hub" in data["links"]:
                lines.append(f"• [GIS Maps]({data['links']['gis_hub']})")
    elif data.get("parcel_id"):
        lines.append(f"📋 **Parcel ID:** {data['parcel_id']}")
        lines.append("")
        if data.get("links"):
            lines.append("**Quick Links:**")
            for name, url in data["links"].items():
                lines.append(f"• [{name.replace('_', ' ').title()}]({url})")
    else:
        lines.append("❌ Address not found in Orange County")
        lines.append("Try the property search manually.")
    
    return "\n".join(lines)


def format_pets_result(data: dict) -> str:
    """Format pet search result for Telegram"""
    lines = ["🐾 **Adoptable Pets**\n"]
    
    if data.get("success"):
        stats = data.get("stats", {})
        if stats:
            lines.append(f"📊 **Shelter Stats:** {stats.get('dogs', '?')} dogs, {stats.get('cats', '?')} cats")
            lines.append(f"✅ **Ready to adopt:** {stats.get('ready_to_adopt', '?')}")
            lines.append("")
        
        pets = data.get("pets", [])
        if pets:
            lines.append("**Available Now:**")
            for pet in pets[:10]:
                status = "✅" if pet.get("ready_to_adopt") else "⏳"
                lines.append(f"{status} **{pet['name']}** ({pet.get('animal_id', 'N/A')})")
            
            if len(pets) > 10:
                lines.append(f"_...and {len(pets) - 10} more_")
        
        lines.append("")
        lines.append(f"🏠 [Visit Shelter]({data.get('shelter_url', '')})")
        lines.append(f"📞 {data.get('contact', '407-836-3111')}")
    else:
        lines.append("❌ Couldn't fetch shelter data")
        lines.append(f"[Try the website]({data.get('shelter_url', '')})")
    
    return "\n".join(lines)


def format_permit_result(data: dict) -> str:
    """Format permit info for Telegram"""
    if data.get("error"):
        return f"❌ {data['error']}\n\nAvailable: {', '.join(data.get('available_types', []))}"
    
    lines = [f"📋 **{data.get('name', 'Permit Info')}**\n"]
    
    if data.get("fee"):
        lines.append(f"💰 **Fee:** {data['fee']}")
    if data.get("review_time"):
        lines.append(f"⏱️ **Review:** {data['review_time']}")
    if data.get("expires"):
        lines.append(f"📅 **Expires:** {data['expires']}")
    if data.get("submit_via"):
        lines.append(f"📤 **Submit:** {data['submit_via']}")
    
    lines.append("")
    
    if data.get("requirements"):
        lines.append("**Requirements:**")
        for req in data["requirements"]:
            lines.append(f"• {req}")
    
    if data.get("height_limits"):
        lines.append("\n**Height Limits:**")
        for area, limit in data["height_limits"].items():
            lines.append(f"• {area.replace('_', ' ').title()}: {limit}")
    
    if data.get("contact"):
        lines.append(f"\n📞 {data['contact']}")
    
    return "\n".join(lines)


def format_bookings_result(data: dict) -> str:
    """Format booking info for Telegram"""
    lines = ["👮 **Daily Bookings**\n"]
    
    if data.get("pdf_available"):
        lines.append(f"✅ Today's booking list is available")
        lines.append(f"📄 [Download PDF]({data.get('bookings_pdf', '')})")
    else:
        lines.append("⏳ Booking list may not be ready yet")
    
    lines.append("")
    lines.append(f"📊 [Population Stats]({data.get('population_stats', '')})")
    lines.append(f"⚖️ [First Appearances]({data.get('first_appearances', '')})")
    lines.append("")
    lines.append(f"_{data.get('note', '')}_")
    
    return "\n".join(lines)


def handle_callback(callback_data: str) -> dict:
    """
    Handle a callback from an inline button.
    Returns: {"text": str, "buttons": list} or {"text": str} for final responses
    """
    parts = callback_data.split(":")
    
    if len(parts) < 2 or parts[0] != "ocfl":
        return {"text": "Unknown action"}
    
    action = parts[1]
    sub_action = parts[2] if len(parts) > 2 else None
    
    # Navigation to flows
    if action in FLOWS and not sub_action:
        flow = FLOWS[action]
        return {
            "text": flow["text"],
            "buttons": flow.get("buttons", [])
        }
    
    # Pets sub-actions
    if action == "pets":
        if sub_action == "dog":
            data = run_ocfl("pets", "--type", "dog", "--limit", "10")
            return {"text": format_pets_result(data)}
        elif sub_action == "cat":
            data = run_ocfl("pets", "--type", "cat", "--limit", "10")
            return {"text": format_pets_result(data)}
        elif sub_action == "ready":
            data = run_ocfl("pets", "--ready", "--limit", "10")
            return {"text": format_pets_result(data)}
        elif sub_action == "stats":
            data = run_ocfl("pets", "--limit", "1")
            return {"text": format_pets_result(data)}
    
    # Permit sub-actions
    if action == "permit" and sub_action:
        data = run_ocfl("permit", sub_action)
        return {"text": format_permit_result(data)}
    
    # Inmate sub-actions
    if action == "inmate":
        if sub_action == "bookings":
            data = run_ocfl("inmate", "--bookings")
            return {"text": format_bookings_result(data)}
        elif sub_action == "appearances":
            return {
                "text": "⚖️ **First Appearances**\n\n[View Schedule](https://netapps.ocfl.net/BestJail/Home/FirstAppearance)"
            }
    
    # Property sub-actions
    if action == "property":
        if sub_action == "parcel_prompt":
            return {
                "text": "🔢 Send me the parcel ID number (e.g., `292234916802030`)",
                "expects_input": True
            }
    
    return {"text": "Action not implemented yet"}


def handle_text_input(text: str, context: str = None) -> dict:
    """
    Handle free text input from user.
    Context can be used to know what flow we're in.
    """
    text = text.strip()
    
    # Check if it looks like a parcel ID
    clean = text.replace("-", "").replace(" ", "")
    if clean.isdigit() and len(clean) >= 12:
        data = run_ocfl("property", text)
        return {"text": format_property_result(data)}
    
    # Otherwise treat as address
    data = run_ocfl("property", text)
    return {"text": format_property_result(data)}


def main():
    """CLI interface for testing the wizard"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  wizard.py callback <callback_data>")
        print("  wizard.py input <text>")
        print("  wizard.py start")
        sys.exit(1)
    
    action = sys.argv[1]
    
    if action == "start":
        result = {"text": FLOWS["main"]["text"], "buttons": FLOWS["main"]["buttons"]}
    elif action == "callback" and len(sys.argv) > 2:
        result = handle_callback(sys.argv[2])
    elif action == "input" and len(sys.argv) > 2:
        result = handle_text_input(" ".join(sys.argv[2:]))
    else:
        print("Invalid arguments")
        sys.exit(1)
    
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
