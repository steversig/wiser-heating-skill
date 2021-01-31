## Voight Kampff tests for wiser-heating-skill

To significantly reduce the time it takes to run these tests and minimise the load on the Wiser Heat Hub it is recommended that you use the caching web server script server4.py

	7 features passed, 0 failed, 0 skipped
 
	64 scenarios passed, 0 failed, 0 skipped

	192 steps passed, 0 failed, 0 skipped, 0 undefined

	Took 0m26.626s

The caching web server use Python **aiohttps** to provide a web server at **localhost:8080** and **requests** to make requests to the real Heat Hub. The requests are cached using **requests-cache**

Change your **hubipaddress** to **localhost:8080** instead of the real one. This can be done at **https://account.mycroft.ai**

## Caching web server Configuration options

Located at top of python script

* Default caching time is 300 seconds (5 minutes)
* The caching server will absord the patching commands if **passPatch = False** and pass them on if **passPatch = True**
* The **heathub = "http://x.x.x.x"** is the address of the real Heat Hub

	./server4.py

## ToDo

Produce an offline version if you don't have a Heat Hub handy for testing
