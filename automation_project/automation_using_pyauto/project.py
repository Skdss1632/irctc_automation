from utility_functions import *


def input_journey_details():
    print("automation started, filling journey details...")
    open_chrome_browser_with_irctc_page()
    click_login_btn()
    source_station = get_booking_details("source_station")
    destination_station = get_booking_details("destination_station")
    travel_date = get_booking_details("travel_date")
    input_source_n_destination_station_n_travel_date(source_station=source_station, destination_station=destination_station, travel_date=travel_date)
    select_ticket_type_from_dropdwn()
    modify_search_loc = wait_for_element(get_image_path("modify_search_image"))
    py.click(modify_search_loc)


def schedule_task_at_specific_time():
    print("click on any coach either sleeper or ac within 3 minute to continue...")
    # click_mouse_position()
    click_on_wl_or_avalible_btn()
    scroll_until_element_visible_not_visible(img_path=get_image_path("book_now_image"), no_of_scrolls=-1)
    click_book_now_inside_select_train(book_now_img_path=get_image_path("book_now_image"))
    # if want to perform any action inside pass details count the presses from gender
    input_passenger_names()
    input_passenger_phn_no()
    if get_ticket_availability_status("is_ticket_available"):
        click_book_only_if_confirm_berth_alloted()
    if get_otp_and_payment_options("is_payment_with_upi"):
        click_pay_with_upi()
    click_continue_btn_inside_pass_details()
    wait_for_element(image_path=get_image_path("review_journey_image"))
    # if ad blocker extension installed on browser no need to sleep here for 1 sec
    # py.sleep(1)
    click_captcha_fld(is_ad_blocker_enabled=True)
    # press (enter key) manually after filling captcha
    wait_for_element(image_path=get_image_path("payment_yellow_image"))
    # if ad blocker extension installed on browser no need to sleep here for 1 sec
    # py.sleep(1)
    if get_otp_and_payment_options("is_payment_with_upi"):
        select_bhim_upi_ssd_for_upi_pay()
        click_pay_n_book(no_of_press=4)
    else:
        click_irctc_e_wallet()
        click_pay_n_book(no_of_press=10)
        # if want to pay with wallet need to click on otp fld otherwise not,
        # if want to pay with upi just scan qr and pay
        click_otp_fld(otp_fld_img_path=get_image_path("otp_fld_image"))
    if get_otp_and_payment_options("is_read_and_write_otp_from_sms"):
        read_n_write_otp_from_kde_sms()


input_journey_details()
schedule_task_at_specific_time()


# if get_coach_booking_preferences("is_ac_3_tier") or get_coach_booking_preferences("is_ac_tier_3_economy"):
#     time = "10:00:00"
# else:
#     time = "11:00:00"
# schedule.every().day.at(time).do(schedule_task_at_specific_time)
# while True:
#     schedule.run_pending()
