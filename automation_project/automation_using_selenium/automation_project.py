from utility_functions import *
open_url()
click_login_btn()
source_station = get_booking_details("source_station")
destination_station = get_booking_details("destination_station")
travel_date = get_booking_details("travel_date")
input_source_n_destination_station_n_travel_date(source_station=source_station, destination_station=destination_station, travel_date=travel_date)
time.sleep(5)




driver.quit()

