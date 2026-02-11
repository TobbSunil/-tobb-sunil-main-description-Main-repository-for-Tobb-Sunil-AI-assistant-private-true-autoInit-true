# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## What Goes Here

Things like:

- Camera names and locations
- SSH hosts and aliases
- Preferred voices for TTS
- Speaker/room names
- Device nicknames
- Anything environment-specific

## Hardware Infrastructure

### Compute
- **Spark1** & **Spark2**: NVIDIA DGX Spark systems
- **Interconnect**: CX7 (Nvidia Quantum InfiniBand)
- **Purpose**: Local LLM inference, offload from Claude

### Networking
- **Spark1 ↔ Spark2**: CX7 interface (high-speed cluster link)

## My Connectivity

### Phone
- **Number:** +46708207537
- **WhatsApp:** Tobb Sunil

### Email
- **Gmail:** tobb.sunil@gmail.com

---

## Examples

```markdown
### Cameras

- living-room → Main area, 180° wide angle
- front-door → Entrance, motion-triggered

### SSH

- home-server → 192.168.1.100, user: admin

### TTS

- Preferred voice: "Nova" (warm, slightly British)
- Default speaker: Kitchen HomePod
```

## Why Separate?

Skills are shared. Your setup is yours. Keeping them apart means you can update skills without losing your notes, and share skills without leaking your infrastructure.

---

Add whatever helps you do your job. This is your cheat sheet.
