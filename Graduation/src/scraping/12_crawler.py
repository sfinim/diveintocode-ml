from get_info import *

base_filename = "yamanashi_nagano.csv"

if __name__ == "__main__":

    with open(base_filename, mode="r") as f:
        url_file = f.read()

    for url_info in url_file.split("\n"):
        if url_info == "":
            continue
        search_tag, base_url = url_info.split(",")

        list_travel_url = get_travel_url(base_url, is_todofuken=True)

        for travel_url in list_travel_url:
            get_travel_info(travel_url, search_tag)

