from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import pandas as pd

def select_from_dropdown(text):
    with open("./find_and_click.js", "r") as file:
        script = file.read()
        driver.execute_script(script, text)

def wait_for_element(selector):
    # Wait for manual login - Adapt the condition if needed
    WebDriverWait(driver, 600).until(  # Adjust timeout if necessary
        EC.presence_of_element_located(selector)
    )


# Kréta url
website_url = "https://klik102382021.e-kreta.hu/"

options = Options()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(options)  # Use the appropriate WebDriver for your browser
driver.get(website_url)

# Wait for manual login - Adapt the condition if needed
wait_for_element(
    (
        By.CSS_SELECTOR,
        "body > div > div.Box-Container > div:nth-child(1) > div.Box-Icon > img",
    )
)

student_name, grade, date, grade_type = "", "", "", ""

df = pd.read_excel("Data.xlsx")
for index, row in df.iterrows():
    student_name = row["Name"]
    grade = row["Grade"]
    date = row["Date"]
    grade_type = row["Type"]

    print(
        f"name: {student_name}, grade: {grade}, date: {date}, grade_type: {grade_type}"
    )

    # Gyereklistás oldal
    grades_url = (
        "https://klik102382021.e-kreta.hu/TanuloErtekeles/Ertekeles/IndexEvkozi"
    )
    driver.get(grades_url)

    # Gyerek kiválasztása listából
    wait_for_element((By.ID, "StartTovabbButton"))
    input("gyerek előtt")
    select_from_dropdown(student_name)
    input("gyerek után")
    driver.find_element(By.ID, "StartTovabbButton").click()
    input("gomb után")

    driver.find_element(
        By.CSS_SELECTOR,
        "#ErtekelesTanuloErtekelesGrid > div > div.kendo-gridFunctionKommand > button.k-button.k-button-icontext.saveErtekeles",
    ).click()

    # Jegy kiválasztása
    driver.execute_script(f"ErtekelesHelper.changeAllOsztalyzatValue(150{grade[-2]});")

    # Dátum beírása
    # date_field = driver.find_element(By.ID, "Datum")
    with open("./write_into_date_field.js", "r") as file:
        driver.execute_script(file.read(), (date))

    # Jegytípus beírása
    select_from_dropdown(grade_type)
    
    # Mentés
    driver.find_element(
        By.CSS_SELECTOR,
        "#ErtekelesTanuloErtekelesGrid > div > div.kendo-gridFunctionKommand > button.k-button.k-button-icontext.saveErtekeles",
    ).click()
    input("asd")

driver.quit()
