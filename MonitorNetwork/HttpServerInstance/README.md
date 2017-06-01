1. This is Python 3 format
2. a httpserver instance based on socket
3. Components: 
   httpserver.py: create httpserver based on socket
   httppost.py: post content to the http server in json/xml format data
   httpget.py: grab content from the http server in json/xml format data
   conf: configure host, server port and content format
   httpserver_pid: record the process id of the http server
4. Current Function:
   httpserver.py: (1)start a http server based on socket, the content can be shown in json or xml; (2)accept requests from httpget.py, httppost.py and browser refresh
   httpget.py: (1)can only get the data in json form (http.client.HTTPException happens, but still can get the data from the exceptMessage); (2)getting data in xml form exists some problem to be solved(TBD)
   httppost.py: (1)can post the data in simple dict form(http.client.HTTPException happens, but data has been posted); (2)but have not used complicated dict data.
