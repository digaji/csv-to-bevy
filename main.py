from os import getenv

from dotenv import load_dotenv
from selenium.webdriver.common.by import By

from src.driver import Driver
from src.parse import parse_csv, save_csv

load_dotenv()


def main():
    user_data_dir = getenv("USER_DATA_DIR")
    profile_dir = getenv("PROFILE_DIRECTORY")
    url = getenv("URL")
    event_name = getenv("EVENT_NAME")
    data = parse_csv(getenv("CSV_FILE"))

    count = 0
    attendees = []

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
        firstName, lastName, email = row["First Name"], row["Last Name"], row["Email"]

        result = driver.add_attendee(
            firstName=firstName,
            lastName=lastName,
            email=email,
        )

        attendees.append(
            {
                "First Name": firstName,
                "Last Name": lastName,
                "Email": email,
                "Success": result,
            }
        )

        count += 1 if result else 0

    driver.click_button(by=By.CSS_SELECTOR, value="[aria-label='Cancel']")

    save_csv(attendees, "results.csv")
    print(
        f"Finished adding attendence of {count} attendees! See full data in results.csv"
    )


if __name__ == "__main__":
    main()
