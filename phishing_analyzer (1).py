import anthropic
import json

client = anthropic.Anthropic()

# real phishing email example (fake apple lockout)
phishing_example = """From: appleid@id-apple-support.com
Subject: Your Apple ID has been locked

Dear Apple User,

Your Apple ID has been locked due to too many failed login attempts.

To unlock your account, you need to verify your information immediately:

http://apple-id-verify.support-login.com/unlock?token=8472hxbq92

If you don't verify within 12 hours, your account will be permanently disabled and all purchases will be lost.

Apple Support Team
© 2024 Apple Inc. All rights reserved."""

# real google security alert (legitimate)
safe_example = """From: no-reply@accounts.google.com
Subject: Security alert for your Google Account

Hi,

We noticed a new sign-in to your Google Account from a Windows device.

If this was you, you don't need to do anything.

If you didn't sign in recently, check your account activity at:
https://myaccount.google.com/notifications

The Google Accounts team"""


def analyze(text):
    prompt = f"""You are a cybersecurity expert analyzing a message for phishing. Analyze the following message and respond ONLY with a JSON object, no markdown or backticks.

Message:
\"\"\"
{text}
\"\"\"

JSON format:
{{
  "verdict": "phishing" | "suspicious" | "safe",
  "riskScore": number 0-100,
  "summary": "one sentence explanation",
  "redFlags": [
    {{ "title": "short flag name", "explanation": "why this is suspicious", "severity": "high" | "medium" | "low" }}
  ],
  "suspiciousLinks": [
    {{ "url": "the url found", "reason": "why it's suspicious" }}
  ],
  "safeIndicators": [
    "thing that looks legitimate"
  ]
}}

Arrays can be empty if nothing applies."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.content[0].text.strip().replace("```json", "").replace("```", "").strip()
    return json.loads(raw)


def show_results(result):
    verdict = result.get("verdict", "unknown").upper()
    score = result.get("riskScore", 0)
    summary = result.get("summary", "")

    icons = {"PHISHING": "🚨", "SUSPICIOUS": "⚠️", "SAFE": "✅"}
    icon = icons.get(verdict, "❓")

    print("\n" + "=" * 60)
    print(f"{icon}  {verdict}  |  Risk Score: {score}/100")
    print(f"   {summary}")
    print("=" * 60)

    flags = result.get("redFlags", [])
    if flags:
        print("\n🚩 Red Flags:")
        for f in flags:
            sev = f.get("severity", "").upper()
            sev_icon = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🔵"}.get(sev, "⚪")
            print(f"\n  {sev_icon} [{sev}] {f.get('title', '')}")
            print(f"     {f.get('explanation', '')}")

    links = result.get("suspiciousLinks", [])
    if links:
        print("\n🔗 Suspicious Links:")
        for l in links:
            print(f"\n  URL:    {l.get('url', '')}")
            print(f"  Reason: {l.get('reason', '')}")

    safe = result.get("safeIndicators", [])
    if safe:
        print("\n✅ Looks Legitimate:")
        for s in safe:
            print(f"  • {s}")

    print()


def main():
    print("Phishing Analyzer")
    print("-" * 30)
    print("1. Paste a message")
    print("2. Use phishing example")
    print("3. Use safe example")

    choice = input("\nPick an option (1/2/3): ").strip()

    if choice == "1":
        print("\nPaste your message. Type END when done:")
        lines = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
        message = "\n".join(lines)
        if not message.strip():
            print("Nothing entered.")
            return
    elif choice == "2":
        message = phishing_example
        print("\nUsing phishing example...")
    elif choice == "3":
        message = safe_example
        print("\nUsing safe example...")
    else:
        print("Invalid option.")
        return

    print("\nAnalyzing...")
    result = analyze(message)
    show_results(result)


if __name__ == "__main__":
    main()
