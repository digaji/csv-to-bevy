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

    driver = Driver(user_data_dir, profile_dir)
    driver.open_page(url)

    # Handle possible Not logged in
    driver.wait_to_load(by=By.LINK_TEXT, value="Log in", timeout=3, click=True)

    # Go to Community Page Dashboard
    driver.click_button(by=By.LINK_TEXT, value="Dashboard")

    # TODO Handle possible Warning pop up

    # Handle possible Feedback pop up
    driver.wait_to_load(by=By.LINK_TEXT, value="Show me later", timeout=3, click=True)

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

        driver.add_attendee(
            firstName=row["First Name"],
            lastName=row["Last Name"],
            email=row["Email"],
        )


if __name__ == "__main__":
    main()
