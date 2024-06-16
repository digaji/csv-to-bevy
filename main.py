import os

from dotenv import load_dotenv
from selenium.webdriver.common.by import By

from src.driver import Driver
from src.parse import parse_csv

load_dotenv()


def main():
    user_data_dir = os.getenv("USER_DATA_DIR")
    profile_dir = os.getenv("PROFILE_DIRECTORY")
    url = os.getenv("URL")
    event_name = os.getenv("EVENT_NAME")
    data = parse_csv(os.getenv("CSV_FILE"))

    count = 0

    driver = Driver(user_data_dir, profile_dir)
    driver.open_page(url)

    # Handle possible Not logged in
    driver.wait_to_load(by=By.LINK_TEXT, value="Log in", timeout=1, click=True)

    # Go to Community Page Dashboard
    driver.click_button(by=By.LINK_TEXT, value="Dashboard")

    # TODO Handle possible Warning pop up

    # Handle possible Feedback pop up
    driver.wait_to_load(by=By.LINK_TEXT, value="Show me later", timeout=1, click=True)

    driver.wait_to_load(
        by=By.XPATH,
        value=f"//*[contains(text(), '{event_name}')]",
        click=True,
    )

    driver.wait_to_load(
        by=By.CSS_SELECTOR, value="[aria-label='Add attendee']", click=True
    )

    for idx in data.index:
        row = data.loc[idx]

        result = driver.add_attendee(
            firstName=row["First Name"],
            lastName=row["Last Name"],
            email=row["Email"],
        )

        count += 1 if result else None

    driver.click_button(by=By.CSS_SELECTOR, value="[aria-label='Cancel']")
    print(f"Finished adding attendence of {count} attendees!")


if __name__ == "__main__":
    main()
