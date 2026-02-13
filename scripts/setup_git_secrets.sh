#!/bin/bash
# setup_git_secrets.sh - Set up encrypted git for OpenClaw secrets

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_DIR="$SCRIPT_DIR/.."

echo "Setting up encrypted git for OpenClaw secrets..."

# Check if age is available
if [ ! -f "/tmp/age/age" ]; then
    echo "Error: age not found at /tmp/age/age"
    echo "Please run: curl -sL https://github.com/FiloSottile/age/releases/download/v1.2.1/age-v1.2.1-linux-amd64.tar.gz | tar xz -C /tmp"
    exit 1
fi

# Create age key if it doesn't exist
AGE_KEY_FILE="$HOME/.config/openclaw/age_key.txt"
AGE_PUB_KEY_FILE="$HOME/.config/openclaw/age_key.pub"

if [ ! -f "$AGE_KEY_FILE" ]; then
    echo "Generating age key..."
    mkdir -p "$HOME/.config/openclaw"
    /tmp/age/age-keygen -o "$AGE_KEY_FILE" 2>/dev/null
    cat "$AGE_KEY_FILE" | grep "# public key:" > "$AGE_PUB_KEY_FILE"
    chmod 600 "$AGE_KEY_FILE"
    echo "Key generated at $AGE_KEY_FILE"
    echo "Public key saved at $AGE_PUB_KEY_FILE"
    echo "Share the public key with other machines that need to decrypt."
fi

# Add age decryption to git hooks
HOOK_DIR="$REPO_DIR/.git/hooks"
mkdir -p "$HOOK_DIR"

cat > "$HOOK_DIR/post-merge" << 'EOF'
#!/bin/bash
# Decrypt secrets after git pull/merge
if [ -f "$HOME/.config/openclaw/age_key.txt" ]; then
    echo "Decrypting secrets after merge..."
    # Add decryption commands here
    # age -d -i $HOME/.config/openclaw/age_key.txt config/openclaw.json.age > config/openclaw.json
fi
EOF

chmod +x "$HOOK_DIR/post-merge"

echo ""
echo "✅ Setup complete!"
echo ""
echo "To encrypt a file for git backup:"
echo "  $SCRIPT_DIR/encrypt_secret.sh <file> <file>.age"
echo ""
echo "To decrypt a file:"
echo "  $SCRIPT_DIR/decrypt_secret.sh <file>.age <file>"
echo ""
echo "Example for openclaw.json:"
echo "  $SCRIPT_DIR/encrypt_secret.sh /home/tobsun/.openclaw/openclaw.json config/openclaw.json.age"
echo "  git add config/openclaw.json.age"
echo ""
