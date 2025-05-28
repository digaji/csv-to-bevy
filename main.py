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

    # # Handle possible Not logged in
    # driver.wait_to_load(by=By.LINK_TEXT, value="Log in", timeout=1, click=True)

    # # Go to Community Page Dashboard
    # driver.click_button(by=By.LINK_TEXT, value="Dashboard")

    # # TODO Handle possible Warning pop up

    # # Handle possible Feedback pop up
    # driver.wait_to_load(by=By.LINK_TEXT, value="Show me later", timeout=3, click=True)

    driver.wait_to_load(
        by=By.XPATH,
        value=f"//*[contains(text(), '{event_name}')]",
        click=True,
    )

    driver.wait_to_load(
        by=By.CSS_SELECTOR,
        value="[aria-label='Add attendee']",
        click=True,
    )

    # Save old data
    data.to_csv("old-data.csv", index=False)

    for idx in data.index:
        print(f"Injecting data of attendee {idx}... {len(data)}\n")
        row = data.loc[idx]
        firstName, lastName, email, isInjected, attendanceStatus = (
            row["First Name"],
            row["Last Name"],
            row["Email Address"],
            row["Inject Status"],
            row["Attendance"] if "Attendance" in row else None,
        )

        if isInjected == "Injected":
            print(f"Data of attendee {email} already injected\n")
            continue
        try:
            # result = driver.add_check_in(firstName, lastName, email, attendanceStatus)
            result = driver.add_attendee(firstName, lastName, email)
        except Exception as e:
            print(f"Error: {e}")
            result = False

        data.at[idx, "Inject Status"] = "Injected" if result else "Failed"

    data.to_csv(getenv("CSV_FILE"), index=False)

    # Count Inject Status Done
    count = data["Inject Status"].value_counts()
    done = count.get("Injected", 0)
    failed = count.get("Failed", 0)

    print(
        f"Finished adding attendence of {len(data)} with {done} successfully data and {failed} failed data attendees! See full data in {getenv('CSV_FILE')}.csv"
    )


if __name__ == "__main__":
    main()
