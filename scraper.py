from selenium import webdriver
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup
import pandas as pd

RESPONSE_WAIT_TIME_SEC = 3


def load_page():
    driver.get("http://cbseaff.nic.in/cbse_aff/schdir_Report/userview.aspx")
    # Use Region Wise Radio Button
    region_radio = driver.find_element_by_xpath("//input[@id='optlist_3']")
    region_radio.click()
    driver.implicitly_wait(RESPONSE_WAIT_TIME_SEC)


# Load the driver and load page
driver = webdriver.Chrome()
load_page()

# Information available for scraping
headers = ['Affiliation Number', 'Name', 'Head/Principal Name', 'Status', 'Affiliated unto', 'Address', 'Phone no.',
           'Email', 'Website']

region_drop_down = Select(driver.find_element_by_xpath("//select[@id='ddlitem']"))
# print(len(region_drop_down.options))

for i in range(1, len(region_drop_down.options)):
    # Define Dataframe for storage
    df = pd.DataFrame(columns=headers)
    # Select regions index wise, 0th indexed option returns no result
    Select(driver.find_element_by_xpath("//select[@id='ddlitem']")).select_by_index(i)
    region_name = Select(driver.find_element_by_xpath("//select[@id='ddlitem']")).first_selected_option.text.title()
    driver.implicitly_wait(RESPONSE_WAIT_TIME_SEC)

    # Click Search to get results after choosing region
    driver.find_element_by_xpath("//input[@id='search']").click()
    driver.implicitly_wait(RESPONSE_WAIT_TIME_SEC)

    # Total number of schools in the region are stored in text field with id lbltotal1
    tot_schools = int(driver.find_element_by_xpath("//span[@id='lbltotal1']").text)
    tot_pages = int(tot_schools / 25) + 1

    for k in range(tot_pages):
        # HTML must be loaded now, use static parsing
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        # The first row is header and a single page has about 25 entries
        schools = soup.select("table#T1 > tbody > tr > td > table", recursive=False)
        schools.pop(0)  # Not a school, Header row
        for school in schools:
            cols = school.tbody.tr.find_all('td', recursive=False)
            col_1, col_2 = cols[1], cols[2]

            col_1_data = col_1.select("table > tbody > tr")
            col_2_data = col_2.select("table > tbody > tr")
            # Affiliation Number
            try:
                aff_no = col_1_data[0].select("td")[0].contents[1]
            except IndexError:
                aff_no = ''
            # Name of School
            try:
                name = col_1_data[1].select("td > a")[0].contents[0]
            except IndexError:
                name = ''
            # Principal Name (Can be empty, handle error)
            try:
                principal_name = col_1_data[2].select("td")[0].contents[1]
            except IndexError:
                principal_name = ''
            # Status of School
            try:
                status = col_1_data[3].select("td")[0].contents[1]
            except IndexError:
                status = ''
            # Affiliation Expiry
            try:
                aff_unto = col_1_data[4].select("td")[0].contents[1].strip()
            except IndexError:
                aff_unto = ''
            # Address of School
            try:
                address = ' '.join(col_2_data[0].select("td")[0].contents[1].strip().split())
            except IndexError:
                address = ''
            # Phone number (Can be empty)
            try:
                phone_no = ' '.join(col_2_data[1].select("td")[0].contents[1].strip().split())
            except IndexError:
                phone_no = 0
            # Misc contact (Can be empty)
            try:
                e_mail = col_2_data[2].select("td")[0].contents[2].strip()
            except IndexError:
                e_mail = ''
            try:
                website = col_2_data[2].select("td")[0].contents[5].strip()
            except IndexError:
                website = ''

            # Add the scraped info to dataframe
            df.loc[len(df)] = ([aff_no, name, principal_name, status, aff_unto, address, phone_no, e_mail, website])
        # Navigate to next page using next button
        btn_next = driver.find_element_by_xpath("//input[@id='Button1']")
        driver.execute_script("arguments[0].click();", btn_next)

    # Sort the dataframe
    name_sorted_df = df.sort_values(by=['Name'], ascending=True)

    # Save using this region's name in Camel case
    csv_name = region_name + '.csv'
    name_sorted_df.to_csv(csv_name, index=False)

    # Website tends to not immediately load for another region, refresh
    load_page()
    Select(driver.find_element_by_xpath("//select[@id='ddlitem']")).select_by_index(i)
    driver.implicitly_wait(RESPONSE_WAIT_TIME_SEC)
driver.close()
