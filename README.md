# fw_apy
Python wrapper for FileWave api.

### Setup
```pip install requests``` if using a trusted ssl cert (will not work with self-signed cert)

```pip install requests[security]``` if using a self-signed cert (will also work with trusted cert)

edit lines 9 & 10 with your encoded API key and server address

The fw_apy.py file can be used on it's own or in oyur own projects. The rest of the files in this repo are examples or supporting files for the examples.


# fw_device_details.py
This is an example of using fw_apy. It is a direct port of the php project from the API training session presented by Tony Keller at the 2017 conference.

### Usage
First, in lines 16-19, replace the query ID's for the OS queries with your own.

```fw_apy.queries()``` will get you a list of all queries on your server with ID numbers

To use it, launch the script, then open your browser to http://localhost:5000

Click on the pie chart to see corresponding clients, then click on client names to get details.

# list_to_query.py
Another example script.
This will generate a single-field query from a list.

### Usage
Edit lines 7-9 to specify the field to search, the path to your list file, and wether to match 'one' or 'all'

As-is it will use a sample list of Mac model names provided by Gilbert Palau and print the raw response with the results of the query to the screen.

See line 33 and beyond for other output options.

