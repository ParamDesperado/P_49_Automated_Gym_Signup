from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    WebDriverException,
    NoSuchElementException,
    TimeoutException,
)
import time
import os

# -------------------- SETUP --------------------
ACCOUNT_EMAIL = "params@testmail.com"
ACCOUNT_PASSWORD = "parampython"
GYM_URL = "https://appbrewery.github.io/gym/"

# Setup Chrome with persistent profile
user_data_dir = os.path.join(os.getcwd(), "chrome_profile")
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 10)


# -------------------- RETRY WRAPPER --------------------
def retry(func, retries=7, description=None):
    """Retries a function if it fails, up to 'retries' times."""
    attempt = 1
    while attempt <= retries:
        try:
            if description:
                print(f"\n🔁 Attempt {attempt}/{retries}: {description}")
            result = func()
            return result
        except (WebDriverException, TimeoutException, Exception) as e:
            print(f"⚠️ {description or func.__name__} failed (attempt {attempt}): {e}")
            time.sleep(2)
            attempt += 1
    print(f"❌ {description or func.__name__} failed after {retries} attempts.\n")
    return None


# -------------------- LOGIN FUNCTION --------------------
def login():
    driver.get(GYM_URL)
    wait.until(EC.element_to_be_clickable((By.ID, "login-button"))).click()

    email_input = wait.until(EC.presence_of_element_located((By.ID, "email-input")))
    email_input.clear()
    email_input.send_keys(ACCOUNT_EMAIL)

    password_input = driver.find_element(By.ID, "password-input")
    password_input.clear()
    password_input.send_keys(ACCOUNT_PASSWORD)

    driver.find_element(By.ID, "submit-button").click()

    wait.until(EC.presence_of_element_located((By.ID, "schedule-page")))
    print("✅ Logged in successfully!")


# -------------------- BOOKING FUNCTION --------------------
def book_classes():
    booked_count = 0
    waitlist_count = 0
    already_count = 0
    processed_count = 0
    detailed_results = []

    class_cards = driver.find_elements(By.CSS_SELECTOR, "div[id^='class-card-']")

    for card in class_cards:
        day_group = card.find_element(By.XPATH, "./ancestor::div[contains(@id, 'day-group-')]")
        day_title = day_group.find_element(By.TAG_NAME, "h2").text

        if "Tue" in day_title or "Thu" in day_title:
            time_text = card.find_element(By.CSS_SELECTOR, "p[id^='class-time-']").text
            if "6:00 PM" in time_text:
                processed_count += 1
                class_name = card.find_element(By.CSS_SELECTOR, "h3[id^='class-name-']").text
                book_button = card.find_element(By.CSS_SELECTOR, "button[id^='book-button-']")
                status = book_button.text.strip()

                if status == "Booked":
                    print(f"✓ Already booked: {class_name} on {day_title}")
                    already_count += 1
                    detailed_results.append(f"[Already Booked] {class_name} on {day_title}")
                elif status == "Waitlisted":
                    print(f"✓ Already on waitlist: {class_name} on {day_title}")
                    already_count += 1
                    detailed_results.append(f"[Already Waitlist] {class_name} on {day_title}")
                elif status == "Book Class":
                    book_button.click()
                    print(f"✅ Successfully booked: {class_name} on {day_title}")
                    booked_count += 1
                    detailed_results.append(f"[New Booking] {class_name} on {day_title}")
                elif status == "Join Waitlist":
                    book_button.click()
                    print(f"🕓 Joined waitlist for: {class_name} on {day_title}")
                    waitlist_count += 1
                    detailed_results.append(f"[New Waitlist] {class_name} on {day_title}")

    print("\n--- BOOKING SUMMARY ---")
    print(f"New bookings: {booked_count}")
    print(f"New waitlist entries: {waitlist_count}")
    print(f"Already booked/waitlisted: {already_count}")
    print(f"Total Tuesday & Thursday 6pm classes: {processed_count}")

    print("\n--- DETAILED CLASS LIST ---")
    for d in detailed_results:
        print(f"  • {d}")

    return processed_count


# -------------------- VERIFICATION FUNCTION --------------------
def get_my_bookings():
    print("\n--- VERIFYING ON MY BOOKINGS PAGE ---")

    my_bookings_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "my-bookings-link"))
    )
    my_bookings_btn.click()

    booked_classes = driver.find_elements(By.CSS_SELECTOR, "div[id^='booking-card-']")
    verified_bookings = []

    for booking in booked_classes:
        try:
            class_name = booking.find_element(By.CSS_SELECTOR, "h3[id^='booking-name-']").text
            time_text = booking.find_element(By.CSS_SELECTOR, "p[id^='booking-time-']").text
            day_text = booking.find_element(By.CSS_SELECTOR, "p[id^='booking-day-']").text

            if ("Tue" in day_text or "Thu" in day_text) and "6:00 PM" in time_text:
                verified_bookings.append(class_name)
                print(f"  ✓ Verified: {class_name}")
        except NoSuchElementException:
            continue

    print(f"\n✅ Found {len(verified_bookings)} Tue/Thu 6 PM bookings.")
    return verified_bookings


# -------------------- MAIN SCRIPT FLOW --------------------
retry(login, retries=7, description="Logging into gym site")
expected_count = retry(book_classes, retries=5, description="Booking classes")
verified = retry(get_my_bookings, retries=5, description="Verifying bookings")

print("\n--- VERIFICATION RESULT ---")
print(f"Expected: {expected_count} bookings")
print(f"Found: {len(verified)} bookings")

if expected_count == len(verified):
    print("✅ SUCCESS: All bookings verified!")
else:
    print(f"❌ MISMATCH: Missing {abs(expected_count - len(verified))} bookings")

# Optional: driver.quit()