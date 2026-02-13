# Encrypted Configs

This directory contains encrypted versions of sensitive OpenClaw configuration files.

## Files

- `openclaw.json.age` - Encrypted main OpenClaw config
- `mcporter.json.age` - Encrypted MCP server config

## Decrypting

```bash
age -d -i ~/.config/openclaw/age_key.txt openclaw.json.age > openclaw.json
age -d -i ~/.config/openclaw/age_key.txt mcporter.json.age > mcporter.json
```

## Security Notes

- Never commit unencrypted config files to git
- Keep your age key file secure (`~/.config/openclaw/age_key.txt`)
- The public key (`age_key.pub`) can be shared with trusted machines
