import requests
import time

# Function to get a CAPTCHA token
def get_captcha_token():
    try:
        response = requests.get("http://localhost:5000/get")  # Adjust port if needed
        return response.text if response.text != "No tokens available" else None
    except:
        print("[-] Error connecting to CAPTCHA server.")
        return None

# Function to send OTP
def send_otp(mobile, country_code):
    url = "https://www.efsanetr.com/api/v2/send/mobileCode"
    data = {
        "mobile": mobile,
        "countryCode": country_code
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K)",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(url, data=data, headers=headers)
    
    if response.status_code == 200:
        print("\n✅ OTP sent successfully! Please check your SMS.")
        return True
    else:
        print("\n❌ Failed to send OTP:", response.text)
        return False

# Function to register an account
def register_account():
    mobile = input("\n📱 Enter your mobile number: ")
    country_code = input("🌍 Enter your country code (e.g., 91 for India): ")

    # Send OTP request
    if not send_otp(mobile, country_code):
        return

    valid_code = input("\n🔢 Enter the OTP received: ")

    captcha_token = get_captcha_token()
    if not captcha_token:
        print("[-] No CAPTCHA tokens available. Solve some CAPTCHAs first.")
        return

    invite_code = "N7BC5L"
    password = "123456A@"

    data = {
        "mobile": mobile,
        "inviteCode": invite_code,
        "cf-turnstile-response": captcha_token,
        "passWord": password,
        "confirmPassWord": password,
        "type": 1,
        "countryCode": country_code,
        "validCode": valid_code
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; K)",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post("https://www.efsanetr.com/api/v2/register", data=data, headers=headers)
    
    if response.status_code == 200:
        print("\n✅ Registration successful!", response.json())
    else:
        print("\n❌ Registration failed:", response.text)

# Run registration process
register_account()
