# DynamicIPManager - Private Dynamic IP Management

This is a Python3 (3.3 & 3.4 only) package containing a server and a client app
for managing your own list of workstations and their dynamic IPs.


##Usage Scenario

I wrote this because I mainly work on my laptop which I carry around different places, but need to ssh into many different workstations that have dynamic IP addresses. Some of the workstations are located overseas and are not registered to a domain (mostly home computers), so when the local router receives a new IP from the ISP, I have no immediate access to the workstation. Rather than resorting to a dynamic DNS service, which would require obtaining additional domains, I thought it would be better to use one of my VPS (registered to a domain) as a "yellow pages" server for my remote workstations. My workstations would report to the VPS at regular interval, and the VPS will keep track of the IP addresses of the client workstations. When I need access to a new IP, I would access the VPS to read the new IP information.

```

+-----------------------------------------------------------------------------------------------------------+
|                                                                                                           |
|                                                                   +--------------------+                  |
|             +---+          request: my name is "workstation 1"    |                    |                  |
|   +---------+   | +---------------------------------------------> |                    |                  |
|   |        ||   |                                                 |                    |                  |
|   |        ||   | <---------------------------------------------+ | +----------------+ |                  |
|   +---------+   |   response: cool, I'm writing down your new IP  | |                | |                  |
|      +--+   +---+                                                 | +----------------+ |                  |
|   workstation 1                                                   |   my hosted VPS    |                  |
|     dynamic IP         +----------------------------------------> |    mydomain.com    |                  |
|   xxx.xxx.xxx.xxx      |   (request sent at interval N secs)      |                    |                  |
|                        |         +------------------------------> |                    |                  |
|                        |         |                                |                    |                  |
|                        |         |                                +-----------+--------+                  |
|             +---+      |         |                                            |                           |
|   +---------+   |      |         |                                         ^  |                           |
|   |        ||   | <----+         |                         request:        |  |  response:                |
|   |        ||   |                |                                 what is |  |    workstation 1's        |
|   +---------+   |                |                         workstation 1's |  |    IP is now:             |
|      +--+   +---+                v                         IP address now? |  |      xxx.xxx.xxx.xxx      |
|   workstation 2                    +---+                                   |  v      updated at hh:mm:ss  |
|     dynamic IP           +---------+   |                                   |                              |
|   xxx.xxx.xxx.xxx        |        ||   |                              +----+-------+                      |
|                          |        ||   |                              |            |                      |
|                          +---------+   |                              |            |                      |
|                             +--+   +---+                              |            |                      |
|                          workstation 3                                +------------+                      |
|                            dynamic IP                                +--------------+                     |
|                          xxx.xxx.xxx.xxx                            +----------------+                    |
|                                                                         my laptop                         |
|                                                                       IP not important                    |
+-----------------------------------------------------------------------------------------------------------+


```

## How to use

The packaged can be `git clone`d or downloaded from pypi via pip3.

```
~$ sudo pip3 install dynipman
```

### Installing on server
```
~$ sudo pip3 install dynipman
~$ dynipman_sd
```
`dynipman_sd` is the server daemon script. This will start the server daemon. The following contents will be created the very first time the server daemon is run:
```
/var/lib/dynipman
      /addressbook.json
      /conf
      /logs.txt
```

After the initial run, `/var/lib/dynipman/conf` should be edited for personal use.
The SHARED_KEY, SERVER, CLIENT, and USE_RSA settings should be edited.
`addressbook.json` is the json file containing all the IP addresses, and the name can be changed in `conf`.
The `conf` file should be copied and used in all the client workstations.


### Installing on client
```
~$ sudo pip3 install dynipman
~$ dynipman_cd
```
`dynipman_cd` is the client daemon script. The first time the client daemon is run, an error will likely be thrown (unless the server daemon was run on the same workstation before).
```
 Connection Error!
   check config at /var/lib/dynipman/conf
   if the config is correct, then the server might be down.
```
Press Ctrl + C to interrupt the daemon, and then copy the `conf` file from the server (or edit the contents so that it is the same as the conf on server)

Now running `dynipman_cd` should be successful:
```
~$ dynipman_cd
2016-mm-dd HH:MM:SS
{'result': 'success', 'data': 'Update saved successfully'}
```

The "yellow pages" can be read by opening up a browser and typing:
```
   http://mydomain.com:7883/
```
The page will display an html page (7883 is the default port number in `conf`)
where you will be able to type in the code (SHARED_KEY in `conf` file) and then press enter to see the list of IPs


If you want, after setting up and confirming connection between server and client, you can register the scripts to be run in the background on startup to make sure these services are always running.


### Using RSA keys

By default, the message that the client sends to the server is encrypted using a symmetrical encryption scheme (AES).

To use asymmetrical encryption (RSA), set the USE_RSA variable in `conf` to True. After this is set to True, RSA keypair will be generated upon executing the scripts (both server and client). Then the server's public key (file name: `server.public`) will need to be copied to `/var/lib/dynipman/` on each client. Conversely, the client's public key (file name: `{CLIENT['name']}.public`) need to be copied to `/var/lib/dynipman/client_keys/` on the server.

When using RSA, the client will fetch a random key upon initial connection. All subsequent messages will be signed with the client's private key, then the entire message is sent encrypted (AES) with the random key. The server will decrypt the message (AES) first with the random key that it issued, and then verify the message with the client's public key.  

* However, the message between the browser and the server is not encrypted.

## Dependencies and Requirements

* Server workstation with a known domain
* tornado (pypi: tornado)
* Crypto (pypi: pycrypto)


## License

MIT License