# Make sure your client email EG(example@example_id.iam.gserviceaccount.com) has 'Read and Analyse' permissions for each property
# for both Analytics and Search Console

# Name: [Analytics view ID, URL, Adwords Campaign ID, Facebook page id]
clientSites = {
            'my first website': ['123456789', 'http://www.myfirstwebsite.com/', '123456789', '123456789012345'],
            'my second website': ['987654321', 'http://www.mysecondwebsite.com/', '987654321', '09876543210987']
        }

# This should be a perminant token, this it more difficult to acquire than a temp token.
FACEBOOK_TOKEN = 'A1B2C3D4E5'