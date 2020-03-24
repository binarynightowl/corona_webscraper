# COVID-19 Web Scraper
This python3 script scrapes COVID-19 data from John Hopkins University and pushes it to a Google Sheets file using Google Clould Platform

## Install

- Download the source code and open the repository:
  ```
  git clone https://github.com/binarynightowl/corona_webscraper.git
  cd corona_webscraper
  ```
- If python3 is not yet installed, follow the proper install directions for your operating system
  - [Mac](https://docs.python-guide.org/starting/install3/osx/)
  - [Linux](https://docs.python-guide.org/starting/install3/linux/)
  - [Windows](https://docs.python-guide.org/starting/install3/win/)
  - Also be sure to install pip
- Install the required dependencies from requirements.txt
  ```
   pip3 install -r requirements.txt
  ```
- Place your Google Cloud Platform API key/credentials (created in the next step) in the projects root folder and name it ```client-secret.json```
  - Be careful to never share your key or upload it to any VCS like GitHub, as it can allow unauthorized users to access your account
  
## Create Google Sheet
- You will need to enable the Google Drive and Google Sheets API in your GoogleCloudPlatform account, and create credentials with the proper privilidges and download the file as a json (and name it accordingly)
  - If you have no idea how to do this, follow the directions at the beginning of the article [here](https://www.twilio.com/blog/2017/02/an-easy-way-to-read-and-write-to-a-google-spreadsheet-in-python.html)
- Create a Google Sheet with the name of ```COVID-19-CasesOverTime```
  - Share your newly created sheet with your API - the email can be found in ```client-secret.json``` and make sure to give it permission to edit the document
    - Example: ```example@project-name.iam.gserviceaccount.com```
- Create 3 different Workbook pages in your sheet
  - The names of the workbook pages will not matter but the first sheet will be used for the World, the second for China, and the third for the US
- The script will write to the sheet regardless, but if you would like, create headings, following this template
   ![example](https://lh3.googleusercontent.com/HhWYlcnWvP2JQzk253I11cK5FDh5uqyjNqYjdV_Ynwe-X9ft4Z7hEn39TJOtm4WqCyJo62QO2IgJyfWBSmT7fTkcm7H576Ij9JJjnxgHjZB7p4aZKXxE1mXgw8rYvD1GtQYCcqpWbr_pzWIK2XquF8lrhEAE_FUuEw1g5DTtng9DT0pXkvAhU2c2eJ_S8BduhHPfC3ImgMr5R1VzK5JgoPkrb3QJFNl1cRFVEM16Q2N0OfL13Zh-8YwqL71fl6mkAjGSxi_isub8fQtTv3J2oVn4CjanFgZTIrK32W2J9jz4VAxgrQaoQ5sECEw3V9JUMAa3pohMqllcPymaa-6uOGgSwIAuoLSMpM71oWa-EgIjk_HmhSbtmLST_BWtH7RFCnitfuRUk6d1NUptxd-rg3H28n0tnmeUWqEPAQ3wIVHtRTZ8BkiL06GDD8vsYlWPiiCwSEMLxtC-o4xxj2sNLFTUyqZPm-3aSLDkc13FTuQ0GrO9fgQeu2aw4JUlek6OKpI0AueAKzAMyCFeZU7Z7jiPTbJVXNe8mJOCMAzoh1uta7T7mXVpQsiKNkn0Jl44D6YpQun2YLZA7kjk9YCbD1QMRRsmrIvNIZFFNVixWi62FqRbgfLyscPIvtBzd_ocBJ2PDbZn9QUJQ4lg_5WVbZ75FaXvZ6FJQTFx-j2XNMOvFLWUrZG4nlYWzz6yfA=w1603-h98-no)
- Delete all of the empty rows
  - The script creates a new row at the end of the document and writes the new data to that, so any blank rows left before will not be written to
Y4ddl312

## Run the Script
- Open a new terminal window (or use the old one if it is still open)
- Open the previously downloaded folder (should be called ```corona_webscraper```)
- Run ```python3 main.py```!


<iframe src="https://services1.arcgis.com/0MSEUqKaxRlEPj5g/ArcGIS/rest/services/Coronavirus_2019_nCoV_Cases/FeatureServer/1/query?where=1=1&outStatistics=[%7B%22statisticType%22:%22sum%22,%22onStatisticField%22:%22Confirmed%22,%22outStatisticFieldName%22:%22confirmed%22%7D,%7B%22statisticType%22:%22sum%22,%22onStatisticField%22:%22deaths%22,%22outStatisticFieldName%22:%22deaths%22%7D,%7B%22statisticType%22:%22sum%22,%22onStatisticField%22:%22recovered%22,%22outStatisticFieldName%22:%22recovered%22%7D]&f=pjson" style="border:0px #ffffff none;" name="myiFrame" scrolling="no" frameborder="1" marginheight="0px" marginwidth="0px" height="400px" width="600px" allowfullscreen></iframe>