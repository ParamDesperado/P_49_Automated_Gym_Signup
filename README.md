# 🏋️‍♂️ Gym Auto-Booking Bot (Selenium Automation)
Automate your gym class bookings for all **Tuesday and Thursday 6:00 PM** sessions using Python + Selenium.

Created by **Param Sangani** 💻  

---

## 🚀 Overview
This script automatically logs into the [App Brewery Gym](https://appbrewery.github.io/gym/) demo site, finds all classes on **Tuesdays and Thursdays at 6 PM**, and:
- Books available classes ✅  
- Joins waitlists 🕓  
- Skips already booked/waitlisted sessions 🚫  
- Verifies your bookings on the **My Bookings** page 🧾  

The script is built with **resilience** in mind — it retries failed actions, handles timeouts, and prints a detailed summary at the end.

---

## 🧩 Features
- 🔐 **Automatic Login** using stored credentials  
- 📅 **Smart Class Detection** for specific days and times  
- 💪 **Retry Logic** for unstable networks or page delays  
- 🧠 **Verification System** to confirm successful bookings  
- 🧾 **Detailed Summary** of all actions taken  
- 💻 **Persistent Chrome Profile** (no need to log in every run)

---

## 🧰 Requirements
Make sure you have the following installed:

- Python **3.8+**
- Google Chrome
- ChromeDriver (matching your Chrome version)
- Selenium
---

## ⚙️ Setup
- Clone this repository
- Edit your credentials inside the script:
  ACCOUNT_EMAIL = "your_email@example.com"
  ACCOUNT_PASSWORD = "your_password"
---
🧩 Tech Stack
	•	Python 3
	•	Selenium WebDriver
	•	ChromeDriver
	•	WebDriverWait & Expected Conditions
	•	Robust Retry Mechanism
---

## 📊 Example Output
🔁 Attempt 1/7: Logging into gym site
✅ Logged in successfully!

✅ Successfully booked: Spin Class on Thu, Aug 14
🕓 Joined waitlist for: Spin Class on Tue, Aug 19

--- BOOKING SUMMARY ---
New bookings: 1
New waitlist entries: 1
Already booked/waitlisted: 0
Total Tuesday & Thursday 6pm classes: 2

--- DETAILED CLASS LIST ---
  • [New Booking] Spin Class on Thu, Aug 14
  • [New Waitlist] Spin Class on Tue, Aug 19

--- VERIFYING ON MY BOOKINGS PAGE ---
  ✓ Verified: Spin Class
  ✓ Verified: Yoga Flow

✅ SUCCESS: All bookings verified!

## 🧑‍💻 Author

- Param Sangani
- Developer | Automation Enthusiast

📧 Contact: param16032006@gmail.com
🌐 GitHub: github.com/ParamDesperado
  
