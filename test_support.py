from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages import LoginPage, MainPage, SupportPage, Logger

# Инициализация драйвера
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()

try:
    # Инициализация страниц
    login_page = LoginPage(driver)
    main_page = MainPage(driver)
    support_page = SupportPage(driver)

    # Авторизация
    driver.get("https://smsfast.net/")
    login_page.click_login_button()
    login_page.enter_credentials("paralysisharmony@gmail.com", "9135678312")
    login_page.submit_login()

    # Шаги теста
    main_page.click_profile_icon()
    main_page.go_to_support()
    Logger.print_success("Все шаги выполнены успешно!")

    support_page.click_new_ticket()
    support_page.enter_subject("Тестовый запрос поддержки 12345")
    support_page.enter_description("Это тестовое описание для запроса в поддержку, чтобы проверить создание тикета.")
    support_page.create_ticket()
    support_page.close_ticket_and_rate()

except Exception as e:
    Logger.print_error(f"Ошибка: {str(e)}")
    driver.save_screenshot("test_error.png")
    Logger.print_error("Сохранен скриншот test_error.png")
    raise

finally:
    Logger.print_step("Завершение работы")
    driver.quit()
    Logger.print_success("Браузер закрыт")