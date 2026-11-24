# Google Tasks setup

Use only when the local script is needed and account authorization is missing.

## One-time setup (user)
1. console.cloud.google.com: create/select a project, enable **Google Tasks API**.
2. Follow the OAuth console’s account/audience requirements for the intended personal access. If tokens expire, diagnose the current app configuration; do not publish an app merely to complete setup.
3. Credentials > Create OAuth client ID > **Desktop app** > download JSON, save locally as `~/.local/share/gtasks/credentials.json` on Debian (Windows: `%LOCALAPPDATA%\gtasks\credentials.json`).
4. Run the full script path above with `auth` and let the user complete OAuth in the browser; never handle credentials or OTPs in chat.

