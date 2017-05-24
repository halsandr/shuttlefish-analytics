import requests
import analytics_config


class facebook_analytics:

    def __init__(self, token, page, chosenDayNum, chosenEndDate):
        self.token = str(token)
        self.page = str(page)
        # Calculating date range
        self.start_date = chosenDayNum.strftime("%Y-%m-%d")
        self.end_date = chosenEndDate.strftime("%Y-%m-%d")

    def fb_impressions(self):
        # The total number of impressions seen of any content associated with your Page.
        response = requests.get('https://graph.facebook.com/v2.9/' + self.page + '/insights/page_impressions?period=day&since='
                                + self.start_date + '&until=' + self.end_date + '&access_token=' + self.token)
        data = response.json()

        impressions = 0

        for i in data.get('data', [])[0].get('values', []):
            impressions += i['value']

        return impressions

    def fb_likes(self):
        # The total number of people who have liked your Page.
        response = requests.get('https://graph.facebook.com/v2.9/' + self.page + '/insights/page_fan_adds?period=day&since='
                                + self.start_date + '&until=' + self.end_date + '&access_token=' + self.token)
        data = response.json()

        likes = 0

        for i in data.get('data', [])[0].get('values', []):
            likes += i['value']

        return likes

    def fb_engagement(self):
        # The number of times people clicked on any of your content.
        response = requests.get('https://graph.facebook.com/v2.9/' + self.page + '/insights/page_consumptions?period=day&since='
                                + self.start_date + '&until=' + self.end_date + '&access_token=' + self.token)
        data = response.json()

        engagements = 0

        for i in data.get('data', [])[0].get('values', []):
            engagements += i['value']

        return engagements

    def test_return(self):
        print self.fb_engagement()


if __name__ == '__main__':
    print "Running facebook test"
    token = analytics_config.FACEBOOK_TOKEN
    page = 835153196540503
    chosenDayNum = "2017-04-05"
    chosenEndDate = "2017-04-11"
    test = facebook_analytics(token, page, chosenDayNum, chosenEndDate)
    test.test_return()
    exit(0)
