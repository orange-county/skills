# Orange County FL Skills

Clawdbot skills for interacting with Orange County, Florida government services.

## Available Skills

### [ocfl](./ocfl/)
Orange County FL Government Services CLI — property lookup, permits, inmate search, pet adoption.

**Features:**
- 🏠 Property geocoding via ArcGIS
- 📋 Permit information (fence, pool, roof, ADU, etc.)
- 🐕 Live shelter pet scraping
- 👮 Inmate/booking lookup

## Installation

Copy the skill folder to your Clawdbot skills directory:

```bash
cp -r ocfl ~/.clawdbot/skills/
```

Or add to your `clawdbot.toml`:

```toml
[[skills]]
path = "/path/to/ocfl"
```

## License

MIT
