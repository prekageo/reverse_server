## Reverse Server – A utility to bypass firewalls

You may find yourself in a situation that you want to access an SSH server which is located behind a firewall. The usual case would be to open port 22 so that you can connect to your server remotelly with your SSH client. There is, though, the possibility that you do not have access to the firewall rules or you are not allowed to change them. There is a workaround for this problem.

Instead of connecting your client to the server, you can connect your server to the client. It looks a bit odd but actually works. You, just, need to setup a cron job so that, e.g., every day at 10 am your server tries to connect to your client. You, also, need a small piece of software: the reverse server. The reverse server is responsible for handling the reversed initiation of the communication so that your SSH client and the SSH server work out of the box (just like when you connect the SSH client to the SSH server).

You can find details about the technique of the reverse server in the following presentation:

[http://docs.google.com/present/view?id=dfrqz4pd\_50dwm7bsf8](http://docs.google.com/present/view?id=dfrqz4pd_50dwm7bsf8)

I have used this utility to connect to SSH servers, but it could also be useful to connect to services that work over the TCP protocol and which require one port in order to function. It gets more complicated if the service needs to open 2 or more ports.
