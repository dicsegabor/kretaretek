from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd

from yaml import safe_load


def select_from_dropdown(driver, text):
    with open("find_and_click.js", "r") as file:
        driver.execute_script(file.read(), (text))


def wait_for_element(driver, selector):
    # Wait for manual login - Adapt the condition if needed
    WebDriverWait(driver, 600).until(  # Adjust timeout if necessary
        EC.presence_of_element_located(selector)
    )


if __name__ == "__main__":
    # Load config
    with open("config.yaml", "r") as file:
        config = safe_load(file)

    selectors = {
        "login_confirm_image": (
            By.CSS_SELECTOR,
            "body > div > div.Box-Container > div:nth-child(1) > div.Box-Icon > img",
        ),
        "save_grade_button": (
            By.CSS_SELECTOR,
            "#ErtekelesTanuloErtekelesGrid > div > div.kendo-gridFunctionKommand > button.k-button.k-button-icontext.saveErtekeles",
        ),
    }

    # Setup driver
    driver = webdriver.Chrome()
    driver.get(config["url"]["main"])

    # Wait for manual login - Adapt the condition if needed
    wait_for_element(driver, selectors["login_confirm_image"])

    df = pd.read_excel(config["datafile"])
    for row in df.iterrows():
        student_name = row["Name"]
        grade = row["Grade"]
        date = row["Date"]
        grade_type = row["Type"]

        driver.get(config["url"]["child_listbox"])

        ###### Gyereklistás oldal ######
        wait_for_element(driver, (By.ID, "StartTovabbButton"))

        # Gyerek kiválasztása listából
        select_from_dropdown(driver, student_name)
        driver.find_element(By.ID, "StartTovabbButton").click()

        ###### Gyerek oldal ######
        wait_for_element(driver, selectors["save_grade_button"])

        # Jegy kiválasztása
        driver.find_element(By.XPATH, f'//*[@title="{grade}"]').click()

        # Dátum beírása
        with open("write_into_date_field.js", "r") as file:
            driver.execute_script(file.read(), (date))

        # Jegytípus beírása
        select_from_dropdown(driver, grade_type)

        # Mentés
        driver.find_element(selectors["save_grade_button"]).click()

    driver.quit()
