from get_info import *

base_filename = "tag_url_3.csv"

if __name__ == "__main__":

    with open(base_filename, mode="r") as f:
        url_file = f.read()

    for url_info in url_file.split("\n"):
        if url_info == "":
            continue
        search_tag, base_url = url_info.split(",")

        list_travel_url = get_travel_url(base_url)

        for travel_url in list_travel_url:
            get_travel_info(travel_url, search_tag)

