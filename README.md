# 🛡️ Phishing Analyzer

A command-line tool that uses Claude AI to analyze emails and messages for phishing attempts, suspicious links, and social engineering tactics.

## Features

- **AI-powered analysis** via the Anthropic Claude API
- **Risk scoring** from 0–100 with a clear verdict: `PHISHING`, `SUSPICIOUS`, or `SAFE`
- **Red flag detection** with severity levels (High / Medium / Low)
- **Suspicious link extraction** with reasons
- **Safe indicator recognition** to reduce false positives
- Built-in example messages for quick testing


   



You'll be prompted to choose an input method:

```
Phishing Analyzer
------------------------------
1. Paste a message
2. Use phishing example
3. Use safe example

Pick an option (1/2/3):
```

| Option | Description |
|--------|-------------|
| `1` | Paste any email or message manually (type `END` on a new line to finish) |
| `2` | Run against a built-in fake Apple phishing email |
| `3` | Run against a built-in legitimate Google security alert |

## Example Output

```
============================================================
🚨  PHISHING  |  Risk Score: 95/100
   Fake Apple support email using an impersonation domain and urgency tactics.
============================================================

🚩 Red Flags:

  🔴 [HIGH] Suspicious Sender Domain
     The sender uses "id-apple-support.com" instead of "apple.com".

  🔴 [HIGH] Urgency / Threat Language
     Claims account will be "permanently disabled" within 12 hours to pressure action.

  🟡 [MEDIUM] Misleading Link
     The unlock link points to "support-login.com", unrelated to Apple.

🔗 Suspicious Links:

  URL:    http://apple-id-verify.support-login.com/unlock?token=8472hxbq92
  Reason: Domain does not belong to Apple; uses a deceptive subdomain structure.
```

