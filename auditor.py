import hashlib
import requests
import getpass
import sys

def check_pwned(password):
    """Check if password has been in a data breach using HIBP API"""
    sha1 = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]
    
    url = f"https://api.pwnedpasswords.com/range/{prefix}"
    response = requests.get(url, headers={"Add-Padding": "true"})
    
    hashes = (line.split(':') for line in response.text.splitlines())
    for h, count in hashes:
        if h == suffix:
            return int(count)
    return 0

def score_password(password):
    """Score password strength 0-100"""
    score = 0
    feedback = []

    # Length scoring
    if len(password) >= 16:
        score += 30
    elif len(password) >= 12:
        score += 20
    elif len(password) >= 8:
        score += 10
    else:
        feedback.append("Too short (use 12+ characters)")

    # Complexity scoring
    if any(c.isupper() for c in password):
        score += 15
    else:
        feedback.append("Add uppercase letters")

    if any(c.islower() for c in password):
        score += 15
    else:
        feedback.append("Add lowercase letters")

    if any(c.isdigit() for c in password):
        score += 15
    else:
        feedback.append("Add numbers")

    if any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        score += 25
    else:
        feedback.append("Add special characters (!@#$% etc)")

    return score, feedback

def get_strength_label(score):
    if score >= 80:
        return "STRONG"
    elif score >= 50:
        return "MODERATE"
    else:
        return "WEAK"

def audit_password(password):
    score, feedback = score_password(password)
    strength = get_strength_label(score)
    pwned_count = check_pwned(password)

    print("\n" + "="*50)
    print(f"  PASSWORD AUDIT REPORT")
    print("="*50)
    print(f"  Strength Score : {score}/100")
    print(f"  Strength Label : {strength}")
    
    if pwned_count > 0:
        print(f"  Breach Status  : ⚠️  COMPROMISED ({pwned_count:,} times)")
    else:
        print(f"  Breach Status  : ✅ Not found in known breaches")

    if feedback:
        print(f"\n  Suggestions:")
        for tip in feedback:
            print(f"    • {tip}")
    else:
        print(f"\n  No suggestions — solid password!")

    print("="*50 + "\n")

def main():
    print("\n🔐 Password Security Auditor")
    print("Checks strength + known data breaches\n")

    if len(sys.argv) > 1:
        # Accept passwords as command line arguments
        passwords = sys.argv[1:]
        for pw in passwords:
            audit_password(pw)
    else:
        # Interactive mode
        while True:
            password = getpass.getpass("Enter password to audit (or Ctrl+C to quit): ")
            if password:
                audit_password(password)
            
            again = input("Audit another? (y/n): ").strip().lower()
            if again != 'y':
                break

if __name__ == "__main__":
    main()