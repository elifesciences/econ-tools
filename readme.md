# ppp-feeder

### Configuration

You must set the following environment variables before running the program (AWS_PROFILE is optiona):

* AWS_ACCESS_KEY_ID The access key for your AWS account.
* AWS_SECRET_ACCESS_KEY The secret key for your AWS account.
* AWS_DEFAULT_REGION The default region to use, e.g. us-east-1.
* AWS_PROFILE The default credential and configuration profile to use, if any. (optional)

### Operation

Usage:
ppp-feeder.py [options] bucket_name

Options:

*  -h, --help  - show this help message and exit
*  -p PREFIX, --prefix=PREFIX   - only feed keys with the given prefix
*  -r RATE, --rate=RATE  - how many seconds between messages
*  -f FILTER, --filter=FILTER  - filter regex to match against keys

The filter option is more flexible than the prefix option but less efficient as the keys are filtered on the client