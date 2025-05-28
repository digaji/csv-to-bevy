import time
import subprocess

import undetected_chromedriver as uc
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

ATTENDANCE = "Used"

def get_chrome_version():
    """
    Get the version of Chrome installed on the system.
    
    Returns:
        int or None: Major Chrome version number or None if not found
    """
    try:
        # Try the Ubuntu/Debian way first
        process = subprocess.Popen(
            ['google-chrome', '--version'], 
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        output, _ = process.communicate()
        if process.returncode == 0:
            version_text = output.decode('UTF-8').strip()
            if "Google Chrome" in version_text:
                version_str = version_text.replace('Google Chrome', '').strip()
                return int(version_str.split('.')[0])  # Return only major version number
    except:
        pass

    try:
        # Try the alternative way
        process = subprocess.Popen(
            ['google-chrome-stable', '--version'], 
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        output, _ = process.communicate()
        if process.returncode == 0:
            version_text = output.decode('UTF-8').strip()
            if "Google Chrome" in version_text:
                version_str = version_text.replace('Google Chrome', '').strip()
                return int(version_str.split('.')[0])  # Return only major version number
    except:
        pass
    
    return None  # If we couldn't get the version


class Driver:
    def __init__(self, user_data_dir: str, profile_dir: str) -> None:
        options = uc.ChromeOptions()

        options.add_argument(f"--user-data-dir={user_data_dir}")
        options.add_argument(f"--profile-directory={profile_dir}")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-plugins-discovery")

        # Get the Chrome version installed on the system
        chrome_version = get_chrome_version()
        if chrome_version:
            print(f"Detected Chrome version: {chrome_version}")
        else:
            print("Could not detect Chrome version, using default")

        print("Opening browser...\n")
        # Use the detected Chrome version instead of requiring the latest
        self.driver = uc.Chrome(
            options=options, 
            enable_cdp_events=True,
            version_main=chrome_version  # This will use your installed Chrome version
        )
        self.driver.maximize_window()

    def open_page(self, url: str) -> None:
        print(f"Opening page: {url}\n")
        self.driver.get(url)

    def close_browser(self) -> None:
        self.driver.close()

    def add_input(self, by: By, value: str, text: str, isDelay=True) -> None:
        print(f"Adding input: {text}\n")
        field = self.driver.find_element(by=by, value=value)

        # Clear input field
        field.send_keys([Keys.BACKSPACE] * 1000)

        field.send_keys(text)

        if isDelay:
            time.sleep(1)

    def click_button(self, by: By, value: str, isDelay=True) -> None:
        print(f"Clicking button: {value}\n")
        button = self.driver.find_element(by=by, value=value)
        button.click()

        if isDelay:
            time.sleep(1)

    def wait_to_load(self, by: By, value: str, timeout=5, click=True) -> None:
        print(f"Waiting to load: {value}" + ("\n" if not click else ""))

        try:
            result = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by, value))
            )

            if click:
                print("Clicking button\n")
                result.click()
                time.sleep(1)
        except (NoSuchElementException, TimeoutException):
            print("\n")
            pass
        else:
            pass

    def search_and_checkin(self, email: str):
        print(f"Searching and checking in: {email}\n")
        self.add_input(
            by=By.XPATH,
            value="/html[1]/body[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/input[1]",
            text=email,
            isDelay=True,
        )

        value = "input[aria-label='check in attendee']"
        self.wait_to_load(by=By.CSS_SELECTOR, value=value, timeout=5, click=False)

        time.sleep(5)

        try:
            checklist = self.driver.find_element(
                by=By.CSS_SELECTOR,
                value="/html[1]/body[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[2]/div[1]/div[1]/div[2]/div[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/div[1]/div[1]/div[6]/div[1]/span[1]/span[1]",
            )
        except Exception as e:
            print("Error")
            print(e)
            return False

        if "jss12" in checklist.get_attribute("class").split():
            print(f"Attendee already checked in: {email}\n")
            return True

        try:
            self.click_button(by=By.CSS_SELECTOR, value=value, isDelay=True)
        except Exception as e:
            print(f"Attendee not found: {email}\n")
            print(e)
            return False

        print(f"Attendee checked in: {email}\n")
        return True

    def add_check_in(
        self, firstName: str, lastName: str, email: str, attendanceStatus: str
    ) -> bool:
        print(f"Adding attendee: {firstName} {lastName}\t{email}\n")

        identifiers = {
            "firstName": "s1vcua",
            "lastName": "s1yx3r",
            "email": "s2v3vd",
            "checked": "jss12",
        }

        self.add_input(
            by=By.ID, value=identifiers.get("firstName"), text=firstName, isDelay=False
        )

        self.add_input(
            by=By.ID, value=identifiers.get("lastName"), text=lastName, isDelay=False
        )

        self.add_input(
            by=By.ID, value=identifiers.get("email"), text=email, isDelay=False
        )

        # Check Send Event Email button
        # value='//*[@id="overlay-container"]/div/div/div[2]/form/div/div[4]/div[2]/div/label/span[1]'
        # value='//div[2]//div[1]//label[1]//span[1]//span[1]//input[1]'
        # value = "span[class='MuiButtonBase-root MuiIconButton-root jss11 MuiCheckbox-root MuiCheckbox-colorPrimary Checkbox-styles__checkbox_1x4jm jss12 Mui-checked MuiIconButton-colorPrimary'] input[type='checkbox']"
        value = "div[class='MuiGrid-root MuiGrid-item MuiGrid-grid-xs-12'] div:nth-child(2) div:nth-child(1) label:nth-child(1) span:nth-child(1) span:nth-child(1) input:nth-child(1)"
        send_event = self.driver.find_element(
            By.CSS_SELECTOR,
            value,
        )

        # Uncheck the Event Email button
        if send_event.is_selected():
            print("Sent Event Email is checked")
            send_event.click()

        print("Sent Event Email is not checked")

        value = "div[class='MuiGrid-root MuiGrid-container MuiGrid-spacing-xs-2'] div:nth-child(1) div:nth-child(1) label:nth-child(1) span:nth-child(1) span:nth-child(1) input:nth-child(1)"
        check_in = self.driver.find_element(By.CSS_SELECTOR, value)

        isAttend: bool = True
        if attendanceStatus != ATTENDANCE:
            isAttend = False

        if check_in.is_selected():
            if not isAttend:
                check_in.click()
        else:
            if isAttend:
                check_in.click()

        self.click_button(by=By.CSS_SELECTOR, value="[aria-label='Save and add more']")

        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, f"//*[contains(text(), 'Attendee added')]")
                )
            )

            print("Attendee successfully added!\n")
            time.sleep(1)
            return True
        except (NoSuchElementException, TimeoutException):
            RED = "\033[91m"
            RESET = "\033[0m"

            print(RED + f"Error on attendee: {firstName} {lastName}\t{email}\n" + RESET)
            return False

    def add_attendee(self, firstName: str, lastName: str, email: str) -> bool:
        print(f"Adding attendee: {firstName} {lastName}\t{email}\n")

        identifiers = {
            "firstName": "s1vcua",
            "lastName": "s1yx3r",
            "email": "s2v3vd",
            "checked": "jss12",
        }

        self.add_input(
            by=By.ID, value=identifiers.get("firstName"), text=firstName, isDelay=False
        )

        self.add_input(
            by=By.ID, value=identifiers.get("lastName"), text=lastName, isDelay=False
        )

        self.add_input(
            by=By.ID, value=identifiers.get("email"), text=email, isDelay=False
        )

        # Check Send Event Email button
        # value='//*[@id="overlay-container"]/div/div/div[2]/form/div/div[4]/div[2]/div/label/span[1]'
        # value='//div[2]//div[1]//label[1]//span[1]//span[1]//input[1]'
        # value = "span[class='MuiButtonBase-root MuiIconButton-root jss11 MuiCheckbox-root MuiCheckbox-colorPrimary Checkbox-styles__checkbox_1x4jm jss12 Mui-checked MuiIconButton-colorPrimary'] input[type='checkbox']"
        value = "div[class='MuiGrid-root MuiGrid-item MuiGrid-grid-xs-12'] div:nth-child(2) div:nth-child(1) label:nth-child(1) span:nth-child(1) span:nth-child(1) input:nth-child(1)"
        send_event = self.driver.find_element(
            By.CSS_SELECTOR,
            value,
        )

        if not send_event.is_selected():
            print("Sent Event Email is not checked")
            send_event.click()

        print("Sent Event Email is checked")

        self.click_button(by=By.CSS_SELECTOR, value="[aria-label='Save and add more']")

        try:
            WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, f"//*[contains(text(), 'Attendee added')]")
                )
            )

            print("Attendee successfully added!\n")
            time.sleep(1)
            return True
        except (NoSuchElementException, TimeoutException):
            RED = "\033[91m"
            RESET = "\033[0m"

            print(RED + f"Error on attendee: {firstName} {lastName}\t{email}\n" + RESET)
            return False
