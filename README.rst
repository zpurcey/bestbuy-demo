Best Buy Product Auto Complete Demo
===============

Please notice this is **experimental** (use at your own risk).
Also see "Known Limitations" below.


Installation
------------

Assumptions:

* Elasticsearch is running locally (localhost:9200)
* Tested on Elasticsearch 1.* (the mapping doesn't work on Elasticsearch 2.*)
* Tested on Python 3.4
* Use virtualenv to install Python dependencies
* Best Buy API key available here: https://developer.bestbuy.com/

Clone repo, install virtualenv, install Python dependencies::

    git clone https://github.com/zpurcey/bestbuy-demo
    cd bestbuy-demo
    virtualenv venv
    source ./venv/bin/activate
    pip install -r requirements.txt

Set API Key Environment Variable as assigned by Best Buy (https://developer.bestbuy.com/)::

    export BESTBUY_API_KEY=<your_api_key>

Create index::

    make index

Import Best Buy Product Data::

    make data


Run backend service::

    make backend

Run frontend service::

    make frontend

Point your browser to::

    http://localhost:8000

and search for a product.

Known Limitations
-----------------


License
-------

The code is under MIT license, see LICENSE.
