# vexpidisplay
This program runs a vexdisplay on a raspberry pi
by using the Tournament Manager Web Server to pull data.

Simply go to vex.jammerxd.com and install the tournament manager mod
on the computer running the tournament manager(windows only)

Then start Tournament Manager and the Web Server. 

Before running the program on the pi, please run the install.sh script in bash.

Next, go onto a raspberry pi and run the VEX Display program
and enter the ip address of the tournament manager pc,
preceeded by http:// and proceeded by /division# where #
is a number from 1 to 10. That number is the division number.

So, an example might look like:
http://10.0.14.45/division1

and the raspberry pi would display stats for division1.


This code will be updated as well as builds for future releases.

Please share your changes or contact me if you have questions. (josh.menzel@yahoo.com)
It shouldn't matter which version of linux you are using as long as it's debian based.


I AM NOT RESPONSIBLE FOR ANY DAMAGES DONE BY THIS SOFTWARE! USE AT YOUR OWN RISK!
