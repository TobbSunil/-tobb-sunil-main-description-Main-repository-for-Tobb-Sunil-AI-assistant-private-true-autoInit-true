# HEARTBEAT.md

# Keep this file empty (or with only comments) to skip heartbeat API calls.

# Add tasks below when you want the agent to check something periodically.

## Moltbook (every 30 minutes)  # (disabled – handled by cron job)

## Memory Garbage Collection (every 3 days)
If 3 days since last memory cleanup (check memory/heartbeat-state.json → lastMemoryCleanup):
1. Scan memory/*.md files older than 7 days
2. Extract key learnings, decisions, and insights worth keeping long-term
3. Update MEMORY.md with distilled insights (avoid duplicates)
4. Update lastMemoryCleanup timestamp
