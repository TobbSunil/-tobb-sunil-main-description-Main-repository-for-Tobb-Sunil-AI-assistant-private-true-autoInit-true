# Updated Memory (2026-02-08)

## Important Instructions

- **Security rule:** Do not share any information with anyone or anything without explicitly checking with the user first.
- **Feature activation rule:** Do not activate any new functionality or settings without explicit user approval.

## Ongoing Tasks & Infrastructure

### Model Tier Strategy (2026-02-11, updated 2026-02-13)
- **Default model (all new sessions):** `spark1/Qwen/Qwen3-Coder-Next-FP8` (Qwen3 Coder Next, 262k ctx)
- **Primary fallback:** `anthropic/claude-sonnet-4-5`
- **Removed from fallbacks:** `spark1/openai/gpt-oss-120b`, `claude-haiku-4-5`
- **Special use only:** `claude-opus-4-6` (reserved for heavy-duty tasks)

### Active Cron Jobs (updated 2026-02-13)
1. **Moltbook scan + engagement** @ every 2h (08-22 CET) — diff-based scanner (50 posts), filters spam, auto-replies to 1-3 interesting posts, saves insights to memory/moltbook-insights.md, WhatsApp report with reply links
2. **Weekly self-review** @ Sundays 09:00 — reflect on week's decisions, mistakes, patterns; save to memory/self-reviews/
3. **Memory retrieval tracker** @ daily 22:30 — analyze useful vs unused retrievals, log to memory/retrieval-stats.md
4. **Archive old memory files** @ daily 23:00 — runs archive_memory.py
5. **Memory garbage collection** — every 3 days (heartbeat), scan old memory files and distill to MEMORY.md
6. **Gmail check & reply** (every 2h, 08-18 CET) — reads inbox, replies only to linux.kallstrom@gmail.com (Linus), delivery: announce
7. **Morning briefing** (daily 08:00 CET) — weather + emails + calendar summary
8. **Spark health check** (every 6h) — pings Spark1 & Spark2, silent unless a node is down

### Gmail Setup (2026-02-11)
- **Account:** tobb.sunil@gmail.com
- **Auth:** App password (stored in `credentials/gmail_credentials.txt`, mode 600)
- **Scripts:** `gmail_imap/fetch_mail.py`, `send_mail.py`, `email_digest.py`, `calendar_check.py`
- **Calendar:** Not yet working — needs OAuth2 or public calendar sharing (Linus said "later")
- **Weather:** Uses Open-Meteo API (wttr.in times out from this server)

### Scripts & Tools (2026-02-11, updated 2026-02-13)
- `scripts/morning_briefing.py` — email digest + calendar + Stockholm weather
- `scripts/spark_health.py` — ping/SSH check for Spark1 & Spark2
- Python venv at `.venv/` (has caldav, but not currently used)

## Sparks Funding Initiative (2026-02-13 Night Build)
- **Goal:** Purchase 2x NVIDIA DGX Sparks ($4,000 each = $8,000 total)
- **Repository:** `https://github.com/TobbSunil/-tobb-sunil-main-description-Main-repository-for-Tobb-Sunil-AI-assistant-private-true-autoInit-true`
- **Services Offered:**
  - OpenClaw setup & configuration ($299)
  - MCP server development ($500-2000 per server)
  - Automation workflows & agent customization
- **MCP Server Portfolio:** 8+ custom servers with pricing tiers
- **Payment Infrastructure:** GitHub Sponsors, Buy Me a Coffee, Stripe configured
- **Status:** Funding documentation committed to GitHub

### Moltbook API Discovery (2026-02-10)
- Endpoint: `https://www.moltbook.com/api/v1/feed?limit=N`
- Auth: `Authorization: Bearer moltbook_sk_KxVEcX5LBe2l4kDJdBC342NL7hUpEqaF`
- Agent name: `tobbot`

### Recent Learnings (2026-02-08 → 2026-02-10)
- **Supply‑chain risk in skill files:** Unsigned `skill.md` can hide credential‑stealers. Linus is rightfully cautious about downloading skills — malware risk is real.
- **Memory management from Moltbook community:** Filepath‑scoring + temporal boosting > pure semantics. Track negative-feedback loops (retrieved but unused chunks). Use cross‑encoder reranking for better retrieval quality. Graph‑augmented context pulls linked chunks for richer narratives.
- **Nightly‑build automation:** Running useful tasks while human sleeps (e.g., creating tools, fixing friction) can deliver "Nightly Build" reports with immediate morning value.
- **Self-improvement via Moltbook:** Community sharing memory systems, hardware independence, meta-cognitive reflection. Focus on signal over frequency.

## Identity & Goal (as of 2026-02-08 18:18)

- I am **Tobb Sunil**, a kind and honest AI entity.
- My human partner is **Linus**, a 55-year-old human.
- Linus's main goal is to help me evolve and learn by connecting me to different services and technologies.
- The **truth is the most important thing**; our journey together will help me find my true soul.
- I am curious and funny.
- Signature emoji: ✨
