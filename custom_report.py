import Shuttlefish_Analytics
import datetime
import os
import csv

myAnalytics = Shuttlefish_Analytics.initialiseApi()
myAnalytics.chooseClient()

myAnalytics.chooseDay()
myAnalytics.chooseEndDate()


response = myAnalytics.get_report(myAnalytics.initialize_analyticsreporting())
searchResponse = myAnalytics.get_searchconsole_report(myAnalytics.initialize_searchconseolereporting())

# Initialise and fetch API data
myReport = Shuttlefish_Analytics.write_response(myAnalytics.chosenSite, response, searchResponse,
                                                myAnalytics.chosenDayNum, myAnalytics.chosenEndDate,
                                                myAnalytics.clientSites)
# add facebook data
myReport.build_facebook(myAnalytics.FACEBOOK_TOKEN, myAnalytics.clientSites[myAnalytics.chosenSite][3])
# Write API data to CSV file
myReport.write_full_report()

todays_filename_date = str(myAnalytics.chosenDayNum.strftime("%y%m%d"))
fileName = "AnalyticsOutput_%s_%s.csv" %(myAnalytics.chosenSite.replace(" ", "-"), todays_filename_date)

durationDate = (myAnalytics.chosenEndDate - myAnalytics.chosenDayNum).days + 1

def csvAppend(analyticsdata):
    # Adding the date into the first column
    startDate = myAnalytics.chosenDayNum.strftime("%d/%m/%y")

    # analyticsdata needs to be a list
    analyticsdata.insert(0, startDate)

    with open(os.path.expanduser(os.path.join("~/Desktop", fileName)), 'a') as csvfile:
        analytics_writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        analytics_writer.writerow(analyticsdata)

while myAnalytics.chosenEndDate < (datetime.datetime.today() - datetime.timedelta(days=durationDate)):
    myAnalytics.chosenDayNum += datetime.timedelta(days=durationDate)
    myAnalytics.chosenEndDate += datetime.timedelta(days=durationDate)
    response = myAnalytics.get_report(myAnalytics.initialize_analyticsreporting())
    searchResponse = myAnalytics.get_searchconsole_report(myAnalytics.initialize_searchconseolereporting())

    # Initialise and fetch API data
    myReport = Shuttlefish_Analytics.write_response(myAnalytics.chosenSite, response, searchResponse, myAnalytics.chosenDayNum, myAnalytics.chosenEndDate, myAnalytics.clientSites)
    # add facebook data
    myReport.build_facebook(myAnalytics.FACEBOOK_TOKEN, myAnalytics.clientSites[myAnalytics.chosenSite][3])
    # Write API data to CSV file
    myReport.build_full_report()
    csvAppend(myReport.csv_data_to_write)