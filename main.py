import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Фикстура для инициализации и закрытия драйвера
@pytest.fixture(scope="module")
def setup_driver():
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    yield driver
    driver.quit()

# Тест авторизации
def test_basic_auth(setup_driver):
    driver = setup_driver
    # Вставьте данные для авторизации в URL
    driver.get("http://admin:admin@the-internet.herokuapp.com/basic_auth")
    # Даем время на загрузку страницы
    driver.implicitly_wait(5)
    # Проверяем, что страница содержит текст "Congratulations"
    assert "Congratulations" in driver.page_source, "Ошибка: Авторизация не выполнена"

# Тест работы с чекбоксами
def test_checkboxes(setup_driver):
    driver = setup_driver
    driver.get("https://the-internet.herokuapp.com/checkboxes")
    checkboxes = driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
    for checkbox in checkboxes:
        if not checkbox.is_selected():
            checkbox.click()
    assert all(cb.is_selected() for cb in checkboxes), "Ошибка: Не все чекбоксы выбраны"

# Тест загрузки файла
def test_file_upload(setup_driver):
    driver = setup_driver
    driver.get("https://the-internet.herokuapp.com/upload")
    file_input = driver.find_element(By.ID, "file-upload")
    file_input.send_keys(r"C:\Users\Arseniy\Desktop\WorkaemPythonPrak4\Text.txt")  # Укажите ваш путь к файлу
    driver.find_element(By.ID, "file-submit").click()
    assert "File Uploaded!" in driver.page_source, "Ошибка: файл не загружен"
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

