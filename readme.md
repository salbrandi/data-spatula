Patella, a webservice resource providing easy collection and comparison of data scraped from urls

Made to make mass data aggregation and comparison easy and efficient so users can spend less time visualising and more time understanding


File structure

flask_server - The module which controls the startup and requests from the webservice, the port, address, and processes user input

click_commands - Defines the command line arguments and options for the utility

htmlparser - The heavy lifter of the project: provides a function which scrapes urls provided in the  arguments, looks for download links, downloads them, formats the data, and sends them through the flask service to be manipulated further by user, such as by being graphed by other functions in the module.
