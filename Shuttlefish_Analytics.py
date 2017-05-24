import sys
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
import datetime
from csvOutput import csvdatawriter
from Facebook_Analytics import facebook_analytics
import analytics_config

class initialiseApi:

    def __init__(self):
        self.clientSites = analytics_config.clientSites
        self.SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
        self.SEARCH_SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']
        self.KEY_FILE_LOCATION = 'client_secrets.json'
        self.FACEBOOK_TOKEN = analytics_config.FACEBOOK_TOKEN
        self.chosenSite = None
        self.VIEW_ID = None
        self.chosenDayNum = None
        self.chosenEndDate = None


    def chooseClient(self):

        for num, carehome in enumerate(self.clientSites):
            print "%i: %s" %(num, carehome)

        chosenNum = raw_input("\nPlease select the number you would like: ")

        while (not isinstance(chosenNum, int)):
            try:
                chosenNum = int(chosenNum)
            except ValueError:
                chosenNum = raw_input("\nPlease only type a number: ")

        for num, carehome in enumerate(self.clientSites):
            if num == chosenNum:
                chosenSite = carehome
                break

        try:
            chosenSite
        except NameError:
            print "The number %i was not available." % chosenNum
            sys.exit(1)

        self.chosenSite = chosenSite
        self.VIEW_ID = self.clientSites[chosenSite][0]

    def chooseDay(self):
        defaultStartDate = (datetime.date.today() - datetime.timedelta(days=7)).strftime("%Y-%m-%d")
        chooseStartDay = raw_input("What day would you like the report to start on? (%s): " % defaultStartDate)

        if not chooseStartDay:
            chooseStartDay = defaultStartDate

        try:
            startDate = datetime.datetime.strptime(chooseStartDay, "%Y-%m-%d")
        except ValueError:
            print "%s does not match the format YYY-MM-DD" % chooseStartDay
            exit(1)

        self.chosenDayNum = startDate

    def chooseEndDate(self):

        chooseDayNum = raw_input("How many days would you like to include in the report? (7): ")

        if not chooseDayNum:
            chooseDayNum = "7"

        while (not isinstance(chooseDayNum, int)):
            try:
                chooseDayNum = int(chooseDayNum)
            except ValueError:
                chooseDayNum = raw_input("\nPlease only type a number: ")

        dayRange = datetime.timedelta(days=(chooseDayNum - 1))
        endDate = self.chosenDayNum + dayRange

        self.chosenEndDate = endDate

    def initialize_analyticsreporting(self):
        # Initializes an Analytics Reporting API V4 service object.
        #
        # Returns:
        #   An authorized Analytics Reporting API V4 service object.

        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            self.KEY_FILE_LOCATION, self.SCOPES)

        # Build the service object.
        analytics = build('analytics', 'v4', credentials=credentials)

        return analytics

    def initialize_searchconseolereporting(self):

        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            self.KEY_FILE_LOCATION, self.SEARCH_SCOPES)

        http_auth = credentials.authorize(Http())

        # Build the service object.
        searchConsole = build('webmasters', 'v3', http=http_auth)

        return searchConsole

    def get_report(self, analytics):
        chosenDayNum = self.chosenDayNum.strftime("%Y-%m-%d")
        chosenEndDate = self.chosenEndDate.strftime("%Y-%m-%d")
        VIEW_ID = self.VIEW_ID

        # Queries the Analytics Reporting API V4.

        # Args:
        #   analytics: An authorized Analytics Reporting API V4 service object.
        # Returns:
        #   The Analytics Reporting API V4 response.

        # Build start date string for dateRanges

        return analytics.reports().batchGet(
            body={
                'reportRequests': [
                    {
                        'viewId': VIEW_ID,
                        'dateRanges': [{'startDate': chosenDayNum, 'endDate': chosenEndDate}],
                        'metrics': [{'expression': 'ga:totalEvents'}],
                        'dimensions': [{'name': 'ga:eventCategory'}]
                    },
                    {
                        'viewId': VIEW_ID,
                        'dateRanges': [{'startDate': chosenDayNum, 'endDate': chosenEndDate}],
                        'metrics': [{"expression": "ga:sessions"}, {"expression": "ga:goalConversionRateAll"},
                                    {"expression": "ga:goalCompletionsAll"}],
                        'dimensions': [{"name": "ga:userAgeBracket"}, {"name": "ga:userGender"}]
                    },
                    {
                        'viewId': VIEW_ID,
                        'dateRanges': [{'startDate': chosenDayNum, 'endDate': chosenEndDate}],
                        'metrics': [{'expression': 'ga:goalConversionRateAll'}],
                        'dimensions': [{'name': 'ga:deviceCategory'}]
                    },
                    {
                        'viewId': VIEW_ID,
                        'dateRanges': [{'startDate': chosenDayNum, 'endDate': chosenEndDate}],
                        'metrics': [{'expression': 'ga:sessions'}, {"expression": "ga:goalConversionRateAll"},
                                    {"expression": "ga:goalCompletionsAll"}],
                        'dimensions': [{'name': 'ga:sourceMedium'}]
                    },
                    {
                        'viewId': VIEW_ID,
                        'dateRanges': [{'startDate': chosenDayNum, 'endDate': chosenEndDate}],
                        'metrics': [{'expression': 'ga:impressions'}, {"expression": "ga:adClicks"},
                                    {"expression": "ga:adCost"}, {"expression": "ga:goalCompletionsAll"}],
                        'dimensions': [{'name': 'ga:adwordsCampaignID'}]
                    }]
            }
        ).execute()

    def get_searchconsole_report(self, searchConsole):

        property_uri = self.clientSites[self.chosenSite][1]

        # Query for Search Console API
        return searchConsole.searchanalytics().query(
            siteUrl=property_uri,
            body={
                "startDate": self.chosenDayNum.strftime("%Y-%m-%d"),
                "endDate": self.chosenEndDate.strftime("%Y-%m-%d")
            }
        ).execute()


class write_response:
    def __init__(self, chosenSite, response, searchResponse, chosenDayNum, chosenEndDate, clientSites):
        self.csv_data_to_write = []
        self.chosenSite = chosenSite
        self.chosenDayNum = chosenDayNum
        self.chosenEndDate = chosenEndDate
        self.analyticsReports = response.get('reports', [])
        self.searchConsoleReports = searchResponse
        # This dictionary is used in multiple reports
        # Pre-populating to prevent KeyError
        self.sourceList = ['google / organic', 'google / cpc', '(direct) / (none)',
                           'bing / organic', 'carehome.co.uk / referral', 'berkleycaregroup.co.uk / referral',
                           'facebook.com / referral', 'twitter.com / referral']
        self.sourceData = {}
        for site in self.sourceList:
            self.sourceData[site] = [0, 0.0, 0]
        self.clientSites = clientSites

    def write_sessions_response(self):
        # Picking later report as this metric was a late addition
        sessionReports = self.analyticsReports[3]

        # Write the total value to csv array
        try:
            self.csv_data_to_write.append(int(sessionReports.get('data', {}).get('totals', [])[0].get('values')[0]))
        except KeyError:
            self.csv_data_to_write.append('Error')

    def write_events_response(self):
        # Picking out the Events report
        eventsReports = self.analyticsReports[0]

        # Writing Events Total field to CSV list
        try:
            self.csv_data_to_write.append(int(eventsReports.get('data', {}).get('totals', [])[0].get('values')[0]))
        except KeyError:
            self.csv_data_to_write.append('Error')

        # Dictionary for storing events data
        eventsData = {
            'mailto_link': 0,
            'tel_link': 0,
            'Contact Form': 0,
            'Brochure Download': 0
        }
        # Adding events data into dictionary
        for row in eventsReports.get('data', {}).get('rows', []):
            dimensions = row.get('dimensions', [])
            metrics = row.get('metrics', [])
            eventsData[dimensions[0]] = metrics[0]['values'][0]

        # Write event data to CSV list
        self.csv_data_to_write.append(int(eventsData['mailto_link']))
        self.csv_data_to_write.append(int(eventsData['tel_link']))
        self.csv_data_to_write.append(int(eventsData['Contact Form']))
        self.csv_data_to_write.append(int(eventsData['Brochure Download']))

    def write_demographics_response(self):
        # Picking out Demographics report
        demographicsReports = self.analyticsReports[1]
        total_sessions = int(demographicsReports.get('data', {}).get('totals', [])[0].get('values')[0])

        # Multidimensional Dictionary for storing demographic data
        demographicsData = {}
        ages = ['18-24', '25-34', '35-44', '45-54', '55-64', '65+']
        for age in ages:
            demographicsData[age] = {
                'distribution': 0.0,
                'conversions': 0.0,
                'sessions': 0,
                'male': {
                    'sessions': 0,
                    'conversions': 0.0,
                    'conversions_num': 0
                },
                'female': {
                    'sessions': 0,
                    'conversions': 0,
                    'conversions_num': 0
                }
            }

        # Adding demographic data into dictionary
        for row in demographicsReports.get('data', {}).get('rows', []):
            ageDimensions = row.get('dimensions', [])[0]
            genderDimensions = row.get('dimensions', [])[1]
            sessionsMetrics = row.get('metrics', [])[0]['values'][0]
            conversionsMetrics = row.get('metrics', [])[0]['values'][1]
            conversionsMetricsNum = row.get('metrics', [])[0]['values'][2]

            demographicsData[ageDimensions][genderDimensions]['sessions'] = int(sessionsMetrics)
            demographicsData[ageDimensions][genderDimensions]['conversions'] = float(conversionsMetrics)
            demographicsData[ageDimensions][genderDimensions]['conversions_num'] = int(conversionsMetricsNum)

        # Calculating and adding Age and Gender distribution and Conversion rate to dictionary
        for age in demographicsData:
            ageTotal = demographicsData[age]['male']['sessions'] + demographicsData[age]['female']['sessions']
            try:
                demographicsData[age]['sessions'] = int(ageTotal)
            except ZeroDivisionError:
                demographicsData[age]['sessions'] = 0
            try:
                demographicsData[age]['distribution'] = (float(ageTotal) / total_sessions) * 100
            except ZeroDivisionError:
                demographicsData[age]['distribution'] = 0

            ageConvNum = demographicsData[age]['male']['conversions_num'] + \
                         demographicsData[age]['female']['conversions_num']
            ageSesNum = demographicsData[age]['male']['sessions'] + \
                        demographicsData[age]['female']['sessions']
            try:
                demographicsData[age]['conversions'] = (float(ageConvNum) / ageSesNum) * 100
            except ZeroDivisionError:
                demographicsData[age]['conversions'] = 0

        # Time to write out calculated values to our CSV list
        for age in ages:
            # Write the "Distribution" cell
            self.csv_data_to_write.append("%.2f" % demographicsData[age]['distribution'] + "%")
            # Write to the "Conversion Rate" cell -- Currently disabled
            # self.csv_data_to_write.append("%.2f" % demographicsData[age]['conversions'] + "%")
            # Write to the "Sessions" cell
            self.csv_data_to_write.append(demographicsData[age]['sessions'])
            # Write to the "Gender: Male" cell
            self.csv_data_to_write.append("%.2f" % demographicsData[age]['male']['conversions'] + "%")
            # Write to the "Gender: Female" cell
            self.csv_data_to_write.append("%.2f" % demographicsData[age]['female']['conversions'] + "%")

    def write_device_response(self):
        # Picking out Device report
        deviceReports = self.analyticsReports[2]

        # Creating dictionary to store data
        deviceData = {
            'mobile': 0.0,
            'desktop': 0.0,
            'tablet': 0.0
        }

        # Transfer data from API to dictionary
        for row in deviceReports.get('data', {}).get('rows', []):
            deviceData[row.get('dimensions', [])[0]] = float(row.get('metrics', [])[0]['values'][0])

        # Write data from dictionary to CSV writer
        self.csv_data_to_write.append("%.2f" % deviceData['desktop'] + "%")
        self.csv_data_to_write.append("%.2f" % deviceData['mobile'] + "%")
        self.csv_data_to_write.append("%.2f" % deviceData['tablet'] + "%")

    def write_organic_response(self):
        # Get Sessions by source/medium from Analytics API
        sourceReports = self.analyticsReports[3]

        # Transfer API data to Dictionary
        for row in sourceReports.get('data', {}).get('rows', []):
            self.sourceData[row.get('dimensions', [])[0]] = [int(row.get('metrics', [])[0]['values'][0]),
                                                            float(row.get('metrics', [])[0]['values'][1]),
                                                             int(row.get('metrics', [])[0]['values'][2])]
        # Transfer the session data to the CSV writer
        self.csv_data_to_write.append(self.sourceData['google / organic'][0])

        # Get Organic Impressions from Search Console API
        try:
            organicImpressions = int(self.searchConsoleReports.get('rows', [])[0]['impressions'])
        except IndexError:
            organicImpressions = 0

        # Write the data to the CSV writer
        self.csv_data_to_write.append(organicImpressions)

    def build_facebook(self, token, page):
        self.token = token
        self.page = page

    def write_social_response(self):
        # Creating list to transfer to csv list
        socialData = [0, 0, 0, '$0.00']

        facebook = facebook_analytics(self.token, self.page, self.chosenDayNum, self.chosenEndDate)

        socialData[0] = facebook.fb_impressions()
        socialData[1] = facebook.fb_likes()
        socialData[2] = facebook.fb_engagement()

        for i in socialData:
            self.csv_data_to_write.append(i)

    def write_adwords_response(self):
        # Get Adwords related data from analytics API
        adwordsReports = self.analyticsReports[4]

        campData = {self.clientSites[self.chosenSite][2]: [0, 0, 0.0, 0]}

        for myCamp in adwordsReports.get('data', {}).get('rows', []):
            campData[myCamp.get('dimensions', [])[0]] = [int(myCamp.get('metrics', [])[0]['values'][0]),
                                                      int(myCamp.get('metrics', [])[0]['values'][1]),
                                                    float(myCamp.get('metrics', [])[0]['values'][2]),
                                                     int(myCamp.get('metrics', [])[0]['values'][3])]

        self.csv_data_to_write.append(campData[self.clientSites[self.chosenSite][2]][0])
        self.csv_data_to_write.append(campData[self.clientSites[self.chosenSite][2]][1])
        self.csv_data_to_write.append("$%.2f" % campData[self.clientSites[self.chosenSite][2]][2])
        self.csv_data_to_write.append(campData[self.clientSites[self.chosenSite][2]][3])

    def write_conversions_response(self):
        # Only run this function AFTER write_organic_response()

        # Amalgamating all facebook sources into 1
        for site in self.sourceData.keys():
            if site != 'facebook.com / referral' and 'facebook' in site:
                self.sourceData['facebook.com / referral'][0] += self.sourceData[site][0]
                self.sourceData['facebook.com / referral'][2] += self.sourceData[site][2]
                del self.sourceData[site]
        # Re-calculating Conversion rate
        try:
            self.sourceData['facebook.com / referral'][1] = (float(self.sourceData['facebook.com / referral'][2])
                                                            / float(self.sourceData['facebook.com / referral'][0]))\
                                                            * 100
        except ZeroDivisionError:
            self.sourceData['facebook.com / referral'][1] = 0

        # Write all data to CSV writer
        for site in self.sourceList:
            self.csv_data_to_write.append(self.sourceData[site][0])
            self.csv_data_to_write.append(self.sourceData[site][2])

    def build_full_report(self):
        # Function to run all CSV list builders
        self.write_sessions_response()
        self.write_events_response()
        self.write_demographics_response()
        self.write_device_response()
        self.write_organic_response()
        self.write_social_response()
        self.write_adwords_response()
        self.write_conversions_response()

    def write_full_report(self):
        self.build_full_report()
        # Write csv_data_to_write list to CSV file
        csvdatawriter(self.csv_data_to_write, self.chosenSite, self.chosenDayNum, self.chosenEndDate)


def main():

    myAnalytics = initialiseApi()
    myAnalytics.chooseClient()
    myAnalytics.chooseDay()
    myAnalytics.chooseEndDate()
    response = myAnalytics.get_report(myAnalytics.initialize_analyticsreporting())
    searchResponse = myAnalytics.get_searchconsole_report(myAnalytics.initialize_searchconseolereporting())

    # Initialise and fetch API data
    myReport = write_response(myAnalytics.chosenSite, response, searchResponse, myAnalytics.chosenDayNum, myAnalytics.chosenEndDate, myAnalytics.clientSites)
    # add facebook data
    myReport.build_facebook(myAnalytics.FACEBOOK_TOKEN, myAnalytics.clientSites[myAnalytics.chosenSite][3])
    # Write API data to CSV file
    myReport.write_full_report()


if __name__ == '__main__':
    main()
    raw_input("Your file has been written to your desktop.\n\nHit enter to finish.")
    sys.exit(0)