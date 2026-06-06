import anthropic
import json

client = anthropic.Anthropic()

SAMPLE_PHISHING = """From: appleid@id-apple-support.com
Subject: Your Apple ID has been locked

Dear Apple User,

Your Apple ID has been locked due to too many failed login attempts.

To unlock your account, you need to verify your information immediately:

http://apple-id-verify.support-login.com/unlock?token=8472hxbq92

If you don't verify within 12 hours, your account will be permanently disabled and all purchases will be lost.

Apple Support Team
© 2024 Apple Inc. All rights reserved."""

SAMPLE_SAFE = """From: no-reply@accounts.google.com
Subject: Security alert for your Google Account

Hi,

We noticed a new sign-in to your Google Account from a Windows device.

If this was you, you don't need to do anything.

If you didn't sign in recently, check your account activity at:
https://myaccount.google.com/notifications

The Google Accounts team"""


def analyze_message(text):
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

Only include items in arrays if they exist. Arrays can be empty."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}]
    )

    raw = response.content[0].text.strip().replace("```json", "").replace("```", "").strip()
    return json.loads(raw)


def print_results(result):
    verdict = result.get("verdict", "unknown").upper()
    score = result.get("riskScore", 0)
    summary = result.get("summary", "")

    icons = {"PHISHING": "🚨", "SUSPICIOUS": "⚠️", "SAFE": "✅"}
    icon = icons.get(verdict, "❓")

    print("\n" + "=" * 60)
    print(f"{icon}  Verdict: {verdict}  |  Risk Score: {score}/100")
    print(f"   {summary}")
    print("=" * 60)

    red_flags = result.get("redFlags", [])
    if red_flags:
        print("\n🚩 Red Flags Detected:")
        for flag in red_flags:
            sev = flag.get("severity", "").upper()
            sev_icons = {"HIGH": "🔴", "MEDIUM": "🟡", "LOW": "🔵"}
            sev_icon = sev_icons.get(sev, "⚪")
            print(f"\n  {sev_icon} [{sev}] {flag.get('title', '')}")
            print(f"     {flag.get('explanation', '')}")

    suspicious_links = result.get("suspiciousLinks", [])
    if suspicious_links:
        print("\n🔗 Suspicious Links Found:")
        for link in suspicious_links:
            print(f"\n  URL:    {link.get('url', '')}")
            print(f"  Reason: {link.get('reason', '')}")

    safe_indicators = result.get("safeIndicators", [])
    if safe_indicators:
        print("\n✅ Safe Indicators:")
        for item in safe_indicators:
            print(f"  • {item}")

    print()


def main():
    print("Phishing Message Analyzer")
    print("-" * 30)
    print("1. Paste your own message")
    print("2. Test with a phishing sample")
    print("3. Test with a safe sample")

    choice = input("\nChoose an option (1/2/3): ").strip()

    if choice == "1":
        print("\nPaste your message below. When done, type END on a new line and press Enter:")
        lines = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
        message = "\n".join(lines)
        if not message.strip():
            print("No message entered. Exiting.")
            return
    elif choice == "2":
        message = SAMPLE_PHISHING
        print("\nUsing phishing sample...")
    elif choice == "3":
        message = SAMPLE_SAFE
        print("\nUsing safe sample...")
    else:
        print("Invalid choice. Exiting.")
        return

    print("\nAnalyzing message...")
    result = analyze_message(message)
    print_results(result)


if __name__ == "__main__":
    main()
