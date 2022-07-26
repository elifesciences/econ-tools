# econ-publishing-tools

eLife Continuum publishing process tools

### Installation

`econ-tools` only requires `boto`. A full development environment can be installed using:

    ./install.sh

### Configuration

You must set the following environment variables before running the program:

* `AWS_ACCESS_KEY_ID` The access key for your AWS account.
* `AWS_SECRET_ACCESS_KEY` The secret key for your AWS account.
* `AWS_DEFAULT_REGION` The default region to use, e.g. `us-east-1`.

## econ_dashprop

Sets string properties against versions of articles within the eLife Continuum Dashboard.
An example use for this is updating the `publication-status` property of an article to indicate it should be temporarily 
hidden.

Usage:

    econ_dashprop.py dashboard_queue_name article_id version property_name property_value

Example:

    $ python econtools/econ_dashprop.py prefix-event-property-incoming-queue 00288 1 publication-status hidden

The `publication-status hidden` results in sending the `publication-status` value of `hidden` onto the 
`event-property-incoming-queue` for article `00288`, version `1`. 

That message is then picked up by the dashboard, which results in hiding version `1` of `00288` from the current list of 
articles that are errored or in progress.

## econ_article_feeder

`econ_article_feeder` sends a JSON message into a SQS queue which triggers an [AWS SWF](https://aws.amazon.com/swf/) 
workflow. This workflow looks in the S3 bucket that is passed to `econ_article_feeder` for a zip file with the key that 
is passed to `econ_article_feeder`. This article zip file, if found, is then processed by the eLife Continuum publishing 
workflow.

Usage:

    econ_article_feeder.py [options] bucket_name workflow_starter_queue_name workflow_name
    $ python econtools/econ_article_feeder.py -p elife-14721-vor-r1 -r 1  elife-production-final workflow-starter-queue IngestArticleZip
    
Options:

*  -h, --help  - show this help message and exit
*  -p PREFIX, --prefix=PREFIX   - only feed keys with the given prefix
*  -r RATE, --rate=RATE  - how many seconds between messages
*  -f FILTER, --filter=FILTER  - filter regex to match against keys
*  -w, --working - print a . character for each key fed

The filter option is more flexible than the prefix option but less efficient as the keys are filtered on the client
