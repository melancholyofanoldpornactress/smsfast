import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Класс для логирования с цветами
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    END = '\033[0m'

class Logger:
    @staticmethod
    def print_success(message):
        print(f"{Colors.GREEN}✓ {message}{Colors.END}")

    @staticmethod
    def print_error(message):
        print(f"{Colors.RED}✗ {message}{Colors.END}")

    @staticmethod
    def print_step(message):
        print(f"\n>>> {message}")

# Класс для страницы логина
class LoginPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)

    # Локаторы
    LOGIN_BUTTON = (By.XPATH, '//*[@id="__nuxt"]/div/header/div[2]/div/div/div[2]/button[1]')
    EMAIL_INPUT = (By.XPATH, '/html/body/div[4]/div/div[2]/div/form/div[1]/div[2]/input')
    PASSWORD_INPUT = (By.XPATH, '/html/body/div[4]/div/div[2]/div/form/div[2]/div[2]/input')
    SUBMIT_BUTTON = (By.XPATH, '/html/body/div[4]/div/div[2]/div/form/button')

    def click_login_button(self):
        login_button = self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON))
        login_button.click()

    def enter_credentials(self, email, password):
        email_input = self.wait.until(EC.presence_of_element_located(self.EMAIL_INPUT))
        email_input.send_keys(email)

        password_input = self.wait.until(EC.presence_of_element_located(self.PASSWORD_INPUT))
        password_input.send_keys(password)

    def submit_login(self):
        submit_button = self.wait.until(EC.element_to_be_clickable(self.SUBMIT_BUTTON))
        submit_button.click()
        time.sleep(2)

# Класс для главной страницы
class MainPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    # Локаторы
    PROFILE_ICON = (By.XPATH, '/html/body/div[1]/div/header/div[1]/div/div/div[1]/button[3]')
    SUPPORT_LINK = (By.XPATH, "//div[contains(@class, 'absolute w-full')]//*[contains(text(), 'Поддержка')]")

    def click_profile_icon(self):
        Logger.print_step("Ищем и нажимаем на иконку профиля")
        profile_icon = self.wait.until(EC.element_to_be_clickable(self.PROFILE_ICON))
        profile_icon.click()
        time.sleep(2)
        Logger.print_success("Иконка профиля успешно нажата")

    def go_to_support(self):
        Logger.print_step("Переходим в раздел поддержки")
        support_links = self.wait.until(EC.presence_of_all_elements_located(self.SUPPORT_LINK))
        if support_links:
            support_links[-1].click()
            Logger.print_success("Успешный переход в поддержку")
        else:
            raise Exception("Элемент 'Поддержка' не найден")
        self.wait.until(lambda d: "support" in d.current_url.lower())
        time.sleep(2)

# Класс для страницы поддержки
class SupportPage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)

    # Локаторы
    NEW_TICKET_BUTTON = (By.XPATH, "//a[@href='/support/create' and contains(@class, 'bg-acsent')]")
    SUBJECT_INPUT = (By.XPATH, "//input[contains(@class, 'rounded-full') and @type='text']")
    DESCRIPTION_TEXTAREA = (By.XPATH, "//textarea[contains(@class, 'w-full h-full')]")
    CREATE_TICKET_BUTTON = (By.XPATH, "//button[contains(., 'Создать тикет')]")
    CLOSE_TICKET_BUTTON = (By.XPATH, "//button[.//span[contains(text(), 'Закрыть тикет')]]")
    MODAL = (By.XPATH, "//div[contains(@id, 'headlessui-dialog-panel')]")
    STAR_BUTTONS = (By.XPATH, "//div[contains(@id, 'headlessui-dialog-panel')]//div[contains(@class, 'flex gap-1')]//button[contains(@class, 'w-12 h-12')]")
    YES_BUTTON = (By.XPATH, "//div[contains(@id, 'headlessui-dialog-panel')]//button[contains(@class, 'bg-acsent') and .//span[contains(text(), 'Да')]]")
    FEEDBACK_INPUT = (By.XPATH, "//div[contains(@id, 'headlessui-dialog-panel')]//textarea[contains(@class, 'rounded-lg-xl')]")
    SUBMIT_BUTTON = (By.XPATH, "//div[contains(@id, 'headlessui-dialog-panel')]//button[contains(@class, 'bg-acsent') and .//span[contains(text(), 'Отправить')]]")

    def click_new_ticket(self):
        Logger.print_step("Нажимаем кнопку 'Новый тикет'")
        new_ticket_btn = self.wait.until(EC.element_to_be_clickable(self.NEW_TICKET_BUTTON))
        new_ticket_btn.click()
        Logger.print_success("Кнопка 'Новый тикет' успешно нажата")
        self.wait.until(lambda d: "support/create" in d.current_url.lower())
        time.sleep(1)

    def enter_subject(self, subject):
        Logger.print_step("Вводим тему сообщения")
        subject_input = self.wait.until(EC.presence_of_element_located(self.SUBJECT_INPUT))
        subject_input.clear()
        subject_input.send_keys(subject)
        Logger.print_success("Тема сообщения успешно введена")
        time.sleep(0.5)

    def enter_description(self, description):
        Logger.print_step("Вводим описание проблемы")
        description_textarea = self.wait.until(EC.presence_of_element_located(self.DESCRIPTION_TEXTAREA))
        description_textarea.clear()
        description_textarea.send_keys(description)
        Logger.print_success("Описание проблемы успешно введено")
        time.sleep(0.5)

    def create_ticket(self):
        Logger.print_step("Нажимаем кнопку 'Создать тикет'")
        create_ticket_btn = self.wait.until(EC.element_to_be_clickable(self.CREATE_TICKET_BUTTON))
        Logger.print_success("Кнопка 'Создать тикет' найдена")

        # Проверяем ошибки валидации
        try:
            error_message = self.driver.find_element(By.XPATH, "//div[contains(@class, 'error') or contains(text(), 'ошибка')]")
            Logger.print_error(f"Обнаружена ошибка валидации: {error_message.text}")
            self.driver.save_screenshot("validation_error.png")
            raise Exception("Форма не прошла валидацию")
        except:
            print("Ошибок валидации перед отправкой не найдено, продолжаем")

        # Пробуем отправить форму
        try:
            self.driver.execute_script("arguments[0].click();", create_ticket_btn)
            form = create_ticket_btn.find_element(By.XPATH, "./ancestor::form")
            self.driver.execute_script("arguments[0].submit();", form)
            Logger.print_success("Форма отправлена через JavaScript")
        except:
            print("Не удалось отправить через JavaScript, пробуем нативный клик")
            create_ticket_btn.click()
        Logger.print_success("Кнопка 'Создать тикет' нажата")

        # Проверяем состояние кнопки
        try:
            WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Создать тикет') and @disabled]"))
            )
            Logger.print_error("Кнопка 'Создать тикет' стала неактивной, возможно, форма отправляется")
        except:
            print("Кнопка 'Создать тикет' не стала неактивной, продолжаем")

        # Проверяем перенаправление
        WebDriverWait(self.driver, 20).until(
            lambda d: bool(re.match(r".*/support/\d+$", d.current_url.lower())) or
            "успешно создан" in d.page_source.lower()
        )
        Logger.print_success("Тикет успешно создан!")
        current_url = self.driver.current_url
        print(f"Текущий URL после создания тикета: {current_url}")
        if re.match(r".*/support/\d+$", current_url.lower()):
            Logger.print_success("URL соответствует формату /support/<ID>")
        else:
            Logger.print_error("URL не соответствует формату /support/<ID>")
        time.sleep(2)

    def close_ticket_and_rate(self):
        Logger.print_step("Закрываем тикет и отправляем оценку")
        current_url = self.driver.current_url
        print(f"Текущий URL: {current_url}")
        if not re.match(r".*/support/\d+$", current_url.lower()):
            Logger.print_error("Не на странице тикета! Текущий URL не соответствует формату /support/<ID>")
            self.driver.save_screenshot("wrong_page_error.png")
            raise Exception("Неправильная страница для закрытия тикета")

        Logger.print_step("Ищем кнопку 'Закрыть тикет'")
        close_ticket_btn = self.wait.until(EC.element_to_be_clickable(self.CLOSE_TICKET_BUTTON))
        Logger.print_success("Кнопка 'Закрыть тикет' найдена")
        self.driver.execute_script("arguments[0].click();", close_ticket_btn)
        Logger.print_success("Кнопка 'Закрыть тикет' нажата")
        time.sleep(3)

        Logger.print_step("Проверяем появление модального окна с оценкой")
        self.wait.until(EC.presence_of_element_located(self.MODAL))
        Logger.print_success("Модальное окно с оценкой появилось")

        Logger.print_step("Ставим оценку 4 звезды")
        star_buttons = self.wait.until(EC.presence_of_all_elements_located(self.STAR_BUTTONS))
        print(f"Найдено звезд: {len(star_buttons)}")
        if len(star_buttons) >= 4:
            self.driver.execute_script("arguments[0].click();", star_buttons[3])
            Logger.print_success("Оценка 4 звезды поставлена")
            time.sleep(1)
        else:
            Logger.print_error(f"Найдено только {len(star_buttons)} звезд, ожидалось минимум 4")
            self.driver.save_screenshot("stars_not_found.png")
            raise Exception("Недостаточно звезд для оценки")

        Logger.print_step("Нажимаем кнопку 'Да'")
        yes_btn = self.wait.until(EC.element_to_be_clickable(self.YES_BUTTON))
        self.driver.execute_script("arguments[0].click();", yes_btn)
        Logger.print_success("Кнопка 'Да' нажата")
        time.sleep(1)

        Logger.print_step("Вводим текст в поле 'Что произошло'")
        feedback_input = self.wait.until(EC.presence_of_element_located(self.FEEDBACK_INPUT))
        feedback_input.clear()
        feedback_input.send_keys("1234567891")
        Logger.print_success("Текст '1234567891' введен в поле 'Что произошло'")
        time.sleep(0.5)

        Logger.print_step("Нажимаем кнопку 'Отправить'")
        submit_btn = self.wait.until(EC.element_to_be_clickable(self.SUBMIT_BUTTON))
        self.driver.execute_script("arguments[0].click();", submit_btn)
        Logger.print_success("Кнопка 'Отправить' нажата")
        time.sleep(1)

        WebDriverWait(self.driver, 10).until(
            EC.invisibility_of_element_located(self.SUBMIT_BUTTON)
        )
        Logger.print_success("Модальное окно закрыто, тикет успешно закрыт!")