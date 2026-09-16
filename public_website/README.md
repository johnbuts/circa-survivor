# Circa Survivor — public site

Static snapshot of the hub, Week 2 chip sandbox, hedge, field, entries, and docs. No server.

## Publish (GitHub Pages)

1. From the repo root: `python3 public_website/sync.py`
2. Push to GitHub.
3. Repo **Settings → Pages → Source: GitHub Actions**.

The workflow deploys this folder as the site root. URL: `https://<user>.github.io/<repo>/`.

Free GitHub accounts need a **public** repo for Pages. The live site is public either way. For a private repo, point Cloudflare Pages at `public_website/` instead.

Do not commit `pick_selection/week1/.env`. FanDuel on the site is the bundled `fanduel_odds.json` snapshot only. Refresh that file with `fetch_fd_odds.py`; the Odds API key never goes in the browser.

## Local

```bash
python3 public_website/sync.py
cd public_website
python3 -m http.server 8080
```

Open http://127.0.0.1:8080/
