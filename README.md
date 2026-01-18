# CheckNow: AI Email Alerter 📧🤖

**Stop checking your email.** CheckNow gives you peace of mind by notifying you ONLY when something has **direct personal consequences** (Bills, Tax, Medical, Emergencies) and ignoring the rest.

---

## 🏎️ Fast Track (Beta Testers)
Want to try it without the setup headache?
1.  **Fill this Form**: [Request Beta Access](https://docs.google.com/forms) (I need to add your email to the Google allowlist).
2.  **Run this Command**:
    ```bash
    curl -sSL https://raw.githubusercontent.com/yzzhong19/checknow/main/install_beta.sh | bash
    ```
    *This runs the pre-configured version. You just need a Pushover Key and a Gemini Key.*

---

## 🚀 DIY Start (Self-Hosted)
For power users who want full control...
*   **AI-Powered Filtering**: Uses Gemini Flash to understand context (e.g., "$100M ARR for company" = Ignore vs "Payment Failed" = **URGENT**).
*   **Privacy First**: Runs 100% on **YOUR** computer/server. Your emails are processed locally and never sent to a third-party server.
*   **Emergency Alerts**: Bypasses "Silent Mode" on your phone for critical deadlines (uses Pushover Priority 2).
*   **Rate Limit Smart**: Handles API limits gracefully with exponential backoff.

---

## 🚀 Easy Start (Self-Hosted)

### Prerequisites
1.  **Docker Desktop** (Installed and running).
2.  **Pushover Account** ($5 one-time fee) -> [Get User Key](https://pushover.net/).
3.  **Gemini API Key** (Free) -> [Get Key](https://aistudio.google.com/app/apikey).
4.  **Google OAuth Credentials** (See Setup Guide below).

### Step 1: Configuration
Create a file named `.env` in a folder:
```ini
# Google Credentials
GOOGLE_CLIENT_ID=your_client_id
GOOGLE_CLIENT_SECRET=your_client_secret
GEMINI_API_KEY=your_gemini_key

# Notification Credentials
PUSHOVER_USER_KEY=your_pushover_user_key
PUSHOVER_TOKEN=your_pushover_app_token
```

### Step 2: Authentication (One Time)
Run this command to login to your Gmail:
```bash
docker run -it -v $(pwd):/app -p 8080:8080 yzzhong/checknow:latest python main.py
```
*   Click the link it provides.
*   Login with Gmail.
*   It will save a `token.json` file to your folder.

### Step 3: Run Forever
Create a `docker-compose.yml`:
```yaml
services:
  checknow:
    image: yzzhong/checknow:latest
    restart: unless-stopped
    volumes:
      - ./.env:/app/.env
      - ./token.json:/app/token.json
      - ./storage.json:/app/storage.json
```

Start it:
```bash
touch storage.json
docker compose up -d
```

---

## 🛠️ Advanced Setup: Get Your Own Google Credentials
Since this is a self-hosted app, you should create your own "Project" in Google to identify yourself.

1.  Go to [Google Cloud Console](https://console.cloud.google.com/).
2.  Create a Project named "CheckNow".
3.  Search for "Gmail API" -> Enable it.
4.  Go to **OAuth Consent Screen**:
    *   Type: External.
    *   Add your email to "Test Users".
5.  Go to **Credentials** -> Create OAuth Client ID -> Desktop App.
6.  Download the JSON and put the ID/Secret in your `.env`.

---

## License
MIT License. Free for everyone.
