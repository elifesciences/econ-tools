# econ-publishing-tools

eLife Continuum publishing process tools

### Installation

econ-publishing-tools requires boto. 

    pip install -r requirements.txt 

### Configuration

You must set the following environment variables before running the program:

* AWS_ACCESS_KEY_ID The access key for your AWS account.
* AWS_SECRET_ACCESS_KEY The secret key for your AWS account.
* AWS_DEFAULT_REGION The default region to use, e.g. us-east-1.

A python developemnet environment is required. It is recommended to create a python virtual ennvironment and 
install dependencies from requirements.txt .e.g.
 
    virtualenv venv
    source venv/bin/activate
    pip install -r requirements.txt
    
This environment should be activated when running any of the tools, e.g.

    source venv/bin/activate

## econ_dashprop

econ_dashboard string properties against versions of articles within the eLife Continuum Dashboard.
An example use for this is updating the publication-status property of an article to indicate it should be temporarily hidden.

### Operation

Usage:
```
    econ_dashprop.py dashboard_queue_name article_id version property_name property_value 

    $ python econ_dashprop.py prefix-event-property-incoming-queue 00288 1 publication-status hidden
``` 

## econ_article_feeder

econ_article_feeder sends a JSON message into a SQS queue which triggers an [AWS SWF](https://aws.amazon.com/swf/) workflow. This workflow looks in the S3 bucket that is passed to econ_article_feeder for a zip file with the key that is passed to econ_article_feeder. This article zip file if found is then processed by the eLife Continuum publishing workflow.

### Operation

Usage:
```
    econ_article_feeder.py [options] bucket_name workflow_starter_queue_name workflow_name

    $ python econ_article_feeder.py -p elife-14721-vor-r1 -r 1  elife-production-final workflow-starter-queue IngestArticleZip
```
    
Options:

*  -h, --help  - show this help message and exit
*  -p PREFIX, --prefix=PREFIX   - only feed keys with the given prefix
*  -r RATE, --rate=RATE  - how many seconds between messages
*  -f FILTER, --filter=FILTER  - filter regex to match against keys
*  -w, --working - print a . character for each key fed

The filter option is more flexible than the prefix option but less efficient as the keys are filtered on the client
