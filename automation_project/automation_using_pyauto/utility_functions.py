import pyautogui as py
import json
import pytesseract
from PIL import Image, ImageGrab
import pyperclip
import os
import platform
import schedule


parent_img_path = "irctc_images/"


def load_json(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)


img_config = load_json('../json_config/automation_img_filenames.json')
booking_config = load_json('../json_config/booking_config.json')
login_credentials = load_json('../json_config/login_credentials.json')
passenger_data = load_json('../json_config/passenger_data.json')


def get_coach_booking_preferences(key: str):
    return booking_config["coach_booking_preferences"].get(key)


def get_ticket_type_selection(key: str):
    return booking_config["ticket_type_selection"].get(key)


def get_ticket_availability_status(key: str):
    return booking_config["ticket_availability_status"].get(key)


def get_otp_and_payment_options(key: str):
    return booking_config["otp_and_payment_options"].get(key)


def get_passenger_details():
    return passenger_data["passenger_details"]


def get_booking_details(key: str):
    return booking_config["booking_details"].get(key)


def get_image_path(image_name: str):
    return parent_img_path + img_config["image_file_name"][image_name]


def get_login_credentials(credentials_key: str):
    return login_credentials["credentials"][credentials_key]


def click_browser():
    system = platform.system()
    if system == "Windows":
        os.system("start chrome")
    elif system == "Linux":
        os.system("google-chrome &")
    else:
        raise NotImplementedError("Unsupported operating system")


def open_url():
    py.write("https://www.irctc.co.in/nget/train-search", interval=0.1)
    py.press("enter")


def click_book_now_inside_select_train(book_now_img_path: str):
    book_now_loc = wait_for_element(book_now_img_path)
    py.moveTo(book_now_loc)
    py.click(book_now_loc)


def click_on_wl_or_avalible_btn():
    if get_ticket_availability_status("is_ticket_available"):
        wl_or_available_loc = wait_for_element(get_image_path("available_ticket_image"))
    # if ticket is waiting
    else:
        wl_or_available_loc = wait_for_element(get_image_path("waiting_list_image"))
    py.click(wl_or_available_loc)


def input_passenger_names():
    wait_for_element(image_path=get_image_path("passenger_name_input_fld_image"))
    passenger_details: list = get_passenger_details()
    total_passengers = len(passenger_details)
    for idx, passenger in enumerate(passenger_details):
        passenger_name = passenger.get("NAME")
        py.write(passenger_name)
        py.press("tab")
        py.write(str(passenger.get("AGE")))
        py.press("tab")
        gender_presses = 2 if passenger.get("GENDER") == "Female" else 1
        py.press('right', presses=gender_presses)
        # if passenger name is the last name in list then do not click on add passenger
        if idx < total_passengers - 1:
            py.press("tab", presses=3)
            py.press("enter")
            # there is delay in appearing passenger detail input fld after clicking on add pass detail, so verify the img first then perform action
            wait_for_element(image_path=get_image_path("passenger_name_input_fld_image"))


no_of_press = 0


def click_book_only_if_confirm_berth_alloted():
    global no_of_press
    if get_passenger_phn_no() != "":
        no_of_press = 4
    elif get_passenger_phn_no() == "":
        no_of_press = 10
    py.press("tab", presses=no_of_press)
    # pressing space KEY to select checkbox
    py.press("space")


def click_continue_btn_inside_review_journey(captcha_fill_delay: int, img_path: str):
    scroll_until_element_visible_not_visible(img_path=img_path, no_of_scrolls=3)
    py.sleep(captcha_fill_delay)
    button_location = wait_for_element(image_path=img_path)
    py.click(button_location)


def input_source_n_destination_station_n_travel_date(source_station: str, destination_station: str, travel_date: str):
    # go inside source station input fld
    source_loc = wait_for_element(get_image_path("source_station_image"))
    py.moveTo(source_loc)
    py.click(source_loc)
    py.write(source_station, interval=0.1)
    py.press("enter")

    # go inside destination input fld
    py.press("tab", presses=2)
    py.write(destination_station, interval=0.1)
    py.press("enter")

    # enter travel date
    py.press("tab")
    py.write(travel_date)
    py.press("enter")


def open_chrome_browser_with_irctc_page():
    click_browser()
    # open chrome with shortcut key
    # py.hotkey("shift", "alt", "c")
    # wait_for_element(get_image_path("validate_chrome_open_image"), confidence=0.60, min_search_time=10)
    py.sleep(1)
    py.hotkey("ctrl", "t")
    open_url()


def click_login_btn():
    # verifying that after opening the url login btn is present, if login btn present url loaded successfully otherwise
    # not
    py.sleep(2.5)
    login_btn_loc = wait_for_element(image_path=get_image_path("login_btn_image"))
    py.moveTo(login_btn_loc)
    py.click(login_btn_loc)


def click_pay_n_book(no_of_press: int):
    py.press("tab", presses=no_of_press)
    py.press("enter")


def click_otp_fld(otp_fld_img_path: str):
    wait_for_element(otp_fld_img_path, confidence=0.80, min_search_time=120)
    py.press("tab")


def scroll_until_element_visible_not_visible(img_path: str, no_of_scrolls=-3):
    for _ in range(20):
        py.scroll(no_of_scrolls)
        try:
            if py.locateCenterOnScreen(image=img_path, confidence=0.90) is not None:
                return True
        except py.ImageNotFoundException:
            # Image not found, continue loop
            pass


def click_on_coach_on_selected_train():
    """click on sleeper or third ac or any other coach if you pass img path to this func"""
    coach_type_img_path = ""
    if get_coach_booking_preferences("is_sleeper"):
        coach_type_img_path = get_image_path("sleeper_btn_image")
    elif get_coach_booking_preferences("is_ac_3_tier"):
        coach_type_img_path = get_image_path("ac_3_tier_btn_image")
    elif get_image_path("ac_3_economy_image"):
        coach_type_img_path = get_image_path("ac_3_economy_image")

    btn_location = list(py.locateAllOnScreen(image=coach_type_img_path, grayscale=False, confidence=0.95))
    print(btn_location)
    py.moveTo(btn_location[0])
    py.click(btn_location[0])
    print("total no of sleeper btn visible on ui", len(btn_location))


def click_captcha_fld(is_ad_blocker_enabled: bool):
    if is_ad_blocker_enabled:
        press = 5
    else:
        press = 7
    py.press("tab", presses=press)


def read_and_write_otp_from_mail():
    """this function read and write otp from the mail
    it works only if two tabs are open in browser one is mail and another is irctc web page,
    if you have option read and write otp from the sms if you have linux bcz getting otp on mail sometimes takes time"""
    py.hotkey("ctrl", "tab")
    loc = wait_for_element(get_image_path("otp_txt_in_mail_image"), min_search_time=120)
    py.click(loc)
    wait_for_element(get_image_path("your_one_tym_otp_txt_image"), min_search_time=25)
    py.moveTo(707, 472)
    py.click(707, 472, clicks=2)
    py.hotkey("ctrl", "c")
    # delete the otp mail after copying it
    delete_loc = wait_for_element(get_image_path("delete_icon_of_mail_image"), min_search_time=15)
    py.moveTo(delete_loc)
    py.click(delete_loc)
    py.hotkey("ctrl", "tab")
    otp = pyperclip.paste()
    py.write(otp)
    # go to confirm btn
    py.press("tab")
    print(otp)


def click_pay_with_upi():
    global no_of_press
    passenger_phn_no = get_passenger_phn_no()
    if passenger_phn_no:
        no_of_press = 5
    elif get_ticket_type_selection("is_tatkal") or get_ticket_type_selection("is_premium_tatkal"):
        no_of_press = 6
    # if general
    else:
        no_of_press = 11
    py.press("tab", presses=no_of_press)
    py.press("down")


def click_continue_btn_inside_pass_details():
    global no_of_press
    # if is_payment_with_upi True then cursor is inside pay through bhim upi count the tab press from there
    if get_otp_and_payment_options("is_payment_with_upi"):
        no_of_press = 2
    # if tatkal True then currently cursor is inside this checkbox-- book only if confirm berth are alloted confirm berth
    elif get_ticket_type_selection("is_tatkal") or get_ticket_type_selection("is_premium_tatkal"):
        no_of_press = 8
    elif get_passenger_phn_no():
        no_of_press = 7
    # if not tatkal and phn no == "" then count the tab press from gender box
    else:
        no_of_press = 18
    py.press("tab", presses=no_of_press)
    py.press("enter")


def get_passenger_phn_no():
    return passenger_data.get("passenger_phn_no")


def input_passenger_phn_no():
    passenger_phn_no = get_passenger_phn_no()
    if passenger_phn_no:
        py.press("tab", presses=6)
        py.write(passenger_phn_no)


def wait_for_element(image_path, confidence=0.90, min_search_time=240):
    return py.locateCenterOnScreen(image=image_path, confidence=confidence, minSearchTime=min_search_time)


def click_mouse_position():
    py.click(py.position())


def read_n_write_otp_from_kde_sms():
    # open kde sms
    py.hotkey("ctrl", "alt", "s")
    py.click(wait_for_element(get_image_path("kde_otp_txt_image")))
    py.press("down")
    py.press("enter")
    # wait for the otp
    wait_for_element(get_image_path("kde_connect_blue_color_otp_txt_image"))
    py.click(434, 168, clicks=2)
    py.hotkey("ctrl", "c")
    # close kde sms
    py.hotkey("alt", "f4")
    # open chrome
    py.hotkey("shift", "alt", "c")
    wait_for_element(get_image_path("otp_fld_image"), confidence=0.80)
    otp = pyperclip.paste()
    py.write(otp)
    # go inside continue btn and then hit enter
    # do not remove this comment as of now if remove it maybe book ticket auto if you run program
    # py.press("tab")
    # py.press("enter")
    print(otp)


def get_captcha_text():
    # Take a screenshot (you need to have the image copied to the clipboard)
    screenshot = ImageGrab.grabclipboard()
    if screenshot is not None:
        # Convert the screenshot to grayscale
        gray_screenshot = screenshot.convert('L')

        # Use pytesseract to extract text from the screenshot
        extracted_text = pytesseract.image_to_string(gray_screenshot)
        py.write(extracted_text)


def select_bhim_upi_ssd_for_upi_pay():
    loc = wait_for_element(get_image_path("bhim_upi_txt_image"))
    py.moveTo(loc)
    py.click(loc)
    # click pay using paytm txt
    py.press("tab", presses=2)
    py.press("enter")


def click_irctc_e_wallet():
    wallet_location = wait_for_element(image_path=get_image_path("irctc_e_wallet_image"))
    py.moveTo(wallet_location)
    py.click(wallet_location)
    # verify irctc e wallet btn is clicked
    wait_for_element(get_image_path("an_amt_of_10_applicable_txt_image"))


def select_ticket_type_from_dropdwn():
    if not get_ticket_type_selection("is_general"):
        press = 0
        dropdwn_loc = wait_for_element(get_image_path("ticket_type_dropdwn_image"))
        py.click(dropdwn_loc)
        if get_ticket_type_selection("is_tatkal"):
            press = 2
        if get_ticket_type_selection("is_premium_tatkal"):
            press = 1
        py.press("up", presses=press)
        py.press("enter")

