# CBSE-School-Data-Scraper
Scrapes the CBSE School Data repository region wise. [Scraped data](https://github.com/codejack-CR/CBSE-School-Data-Scraper/tree/main/Scraped%20Data) is available too

URL : http://cbseaff.nic.in/cbse_aff/schdir_Report/userview.aspx

Data available for each "_\<Region\>_.csv"
<pre>
  1.  Affiliation Number
  2.  Name
  3.  Head/Principal Name    (A few values are empty)
  4.  Status                 (A few values are empty)
  5.  Affiliated unto
  6.  Address
  7.  Phone no.              (May be empty)
  8.  Email                  (May be empty)
  9.  Website                (May be empty)
</pre>

_____________________________________________________________________________________
## Dependencies
1. [Selenium](https://pypi.org/project/selenium/)
2. [Chrome](https://www.google.com/intl/en_in/chrome/)
3. [ChromeDriver](https://chromedriver.chromium.org/downloads)
4. [BeautifulSoup](https://pypi.org/project/beautifulsoup4/)
5. [Pandas](https://pypi.org/project/pandas/)

_____________________________________________________________________________________
## Running Instructions
* After all dependencies are satisfied, download [```scraper.py```](https://raw.githubusercontent.com/codejack-CR/CBSE-School-Data-Scraper/main/scraper.py)
* Open Terminal, navigate to download directory and execute 
```console
python scraper.py
```
* CSVs are generated in the working directory

_____________________________________________________________________________________
PS : While the scraper is running, it uses ChromeDriver. A new Chrome window will open and execute tasks automatically. Do not close the window
