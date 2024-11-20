from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By


# Настройка WebDriver
def setup_driver():
    # Используем Service для работы с драйвером
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    return driver


# Тест 1: Проверка авторизации
def test_basic_auth(driver):
    print("Запуск теста: Проверка авторизации...")
    driver.get("https://admin:admin@the-internet.herokuapp.com/basic_auth")  # Вход с базовой авторизацией
    assert "Congratulations" in driver.page_source, "Авторизация не удалась!"
    driver.save_screenshot("basic_auth_success.png")
    print("Тест успешно завершён: Проверка авторизации")


# Тест 2: Работа с чекбоксами
def test_checkboxes(driver):
    print("Запуск теста: Работа с чекбоксами...")
    driver.get("https://the-internet.herokuapp.com/checkboxes")
    checkboxes = driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
    for checkbox in checkboxes:
        if not checkbox.is_selected():
            checkbox.click()
    driver.save_screenshot("checkboxes_checked.png")
    assert all(checkbox.is_selected() for checkbox in checkboxes), "Не все чекбоксы включены!"
    print("Тест успешно завершён: Работа с чекбоксами")


# Тест 3: Загрузка файла
def test_file_upload(driver):
    print("Запуск теста: Загрузка файла...")
    driver.get("https://the-internet.herokuapp.com/upload")
    file_input = driver.find_element(By.ID, "file-upload")
    file_input.send_keys(r"C:\Users\Arseniy\Desktop\WorkaemPythonPrak4\Text.txt")  # Укажите путь к вашему файлу
    driver.find_element(By.ID, "file-submit").click()
    assert "File Uploaded!" in driver.page_source, "Ошибка: файл не был загружен!"
    driver.save_screenshot("file_upload_success.png")
    print("Тест успешно завершён: Загрузка файла")


# Основной блок
def run_tests(close_after_tests=True):
    driver = setup_driver()
    try:
        test_basic_auth(driver)
        test_checkboxes(driver)
        test_file_upload(driver)
    finally:
        if close_after_tests:
            driver.quit()
        else:
            print("Браузер оставлен открытым для анализа.")

if __name__ == "__main__":
    run_tests(close_after_tests=False)
