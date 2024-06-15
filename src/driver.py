import time

import undetected_chromedriver as uc
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class Driver:
    def __init__(self, user_data_dir: str, profile_dir: str) -> None:
        options = uc.ChromeOptions()

        options.add_argument(f"--user-data-dir={user_data_dir}")
        options.add_argument(f"--profile-directory={profile_dir}")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--disable-plugins-discovery")

        print("Opening browser...\n")
        self.driver = uc.Chrome(options=options, enable_cdp_events=True)
        self.driver.maximize_window()

    def open_page(self, url: str) -> None:
        print(f"Opening page: {url}\n")
        self.driver.get(url)

    def close_browser(self) -> None:
        self.driver.close()

    def add_input(self, by: By, value: str, text: str, isDelay=True) -> None:
        print(f"Adding input: {text}\n")
        field = self.driver.find_element(by=by, value=value)
        field.send_keys(text)

        if isDelay:
            time.sleep(1)

    def click_button(self, by: By, value: str, isDelay=True) -> None:
        print(f"Clicking button: {value}\n")
        button = self.driver.find_element(by=by, value=value)
        button.click()

        if isDelay:
            time.sleep(1)

    def wait_to_load(self, by: By, value: str, timeout=10, click=True) -> None:
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

    def add_attendee(self, firstName: str, lastName: str, email: str) -> None:
        print(f"Adding attendee: {firstName} {lastName}\t{email}\n")

        identifiers = {
            "firstName": "s1vcua",
            "lastName": "s1yx3r",
            "email": "s2v3vd",
        }

        # First name
        self.add_input(
            by=By.ID, value=identifiers.get("firstName"), text=firstName, isDelay=False
        )

        # Last name
        self.add_input(
            by=By.ID, value=identifiers.get("lastName"), text=lastName, isDelay=False
        )

        # Email
        self.add_input(
            by=By.ID, value=identifiers.get("email"), text=email, isDelay=False
        )

        # TODO Click Add button
        # TODO Handle possible Error pop up
