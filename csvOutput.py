import csv
import datetime
import os


def csvdatawriter(analyticsdata, chosenSite, chosenDayNum, chosenEndDate):

    # Adding the date into the first column
    startDate = chosenDayNum.strftime("%d/%m/%y")
    todays_filename_date = str(chosenDayNum.strftime("%y%m%d"))
    durationDate = ((chosenEndDate - chosenDayNum).days) + 1

    # analyticsdata needs to be a list
    analyticsdata.insert(0, startDate)

    fileName = "AnalyticsOutput_%s_%s.csv" %(chosenSite.replace(" ", "-"), todays_filename_date)

    with open(os.path.expanduser(os.path.join("~/Desktop", fileName)), 'wb') as csvfile:
        analytics_writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

        # Setting out and spacing out headers for output file
        try:
            # Check 'chosenSite' is defined
            analytics_writer.writerow([
                                       chosenSite,
                                       'Overall',
                                       'Events', '', '', '', '',
                                       'Demographics', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '',
                                       '', '', '', '', '', '', '',
                                       'Device Catagory', '', '',
                                       'Organic', '',
                                       'Social Media', '', '', '', '', '', '', '',
                                       'Conversions', '', '', '', '', '', '', '', '', '', '', '', '', '', ''
                                       ])
        except NameError:
            print "Error: Please remember to define \'chosenName\'"
            exit(1)

        analytics_writer.writerow([
                                   '',
                                   'Total Sessions',
                                   'Total Events', 'Mailto Link', 'Tel Link', 'Contact Form', 'Brochure Download',
                                   '18-24', '', '', '',
                                   '25-34', '', '', '',
                                   '35-44', '', '', '',
                                   '45-54', '', '', '',
                                   '55-64', '', '', '',
                                   '65+', '', '', '',
                                   'Desktop (CR)', 'Mobile (CR)', 'Tablet (CR)',
                                   'Sessions', 'Impressions',
                                   'Facebook', '', '', '', 'Google AdWords', '', '', '',
                                   'Google Organic', '', 'Google CPC', '', 'Direct', '', 'Bing', '',
                                   'Carehome.co.uk', '', 'Berkley Care Group website', '', 'Facebook', '', 'Twitter', ''
                                   ])

        analytics_writer.writerow([
                                   'Over ' + str(durationDate) + ' days',
                                   '',
                                   '', '', '', '', '',
                                   'Distribution', 'Sessions', 'Gender: Male (CR)', 'Gender: Female (CR)',
                                   'Distribution', 'Sessions', 'Gender: Male (CR)', 'Gender: Female (CR)',
                                   'Distribution', 'Sessions', 'Gender: Male (CR)', 'Gender: Female (CR)',
                                   'Distribution', 'Sessions', 'Gender: Male (CR)', 'Gender: Female (CR)',
                                   'Distribution', 'Sessions', 'Gender: Male (CR)', 'Gender: Female (CR)',
                                   'Distribution', 'Sessions', 'Gender: Male (CR)', 'Gender: Female (CR)',
                                   '', '', '', '', '',
                                   'Post Reach', 'Likes', 'Post Engagement', 'Ad spend',
                                   'Impressions', 'Clicks', 'Spend', 'Conversions',
                                   'Sessions', 'Conversions',
                                   'Sessions', 'Conversions',
                                   'Sessions', 'Conversions',
                                   'Sessions', 'Conversions',
                                   'Sessions', 'Conversions',
                                   'Sessions', 'Conversions',
                                   'Sessions', 'Conversions',
                                   'Sessions', 'Conversions'
                                   ])

        # Writing the data into the new line
        analytics_writer.writerow(analyticsdata)

if __name__ == '__main__':
    print "\nRunning csv test"
    chosenSite = "TEST RUN"
    myData = [1, 2, 3, '4', '5', '6']
    chosenDayNum = datetime.datetime.strptime("2017-04-05", "%Y-%m-%d").date()
    chosenEndDate = datetime.datetime.strptime("2017-04-11", "%Y-%m-%d").date()
    csvdatawriter(myData, chosenSite, chosenDayNum, chosenEndDate)
    exit(0)
