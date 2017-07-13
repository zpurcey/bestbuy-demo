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

Clone repo, install virtualenv, install Python dependencies::

    git clone https://github.com/zpurcey/bestbuy-demo
    cd bestbuy-demo
    virtualenv venv
    source ./venv/bin/activate
    pip install -r requirements.txt


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
