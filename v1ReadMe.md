# Automatic Plant Grower
A couple of students at Bristol University got bored and wanted a side project. We like plants so we built this self contained indoor plant grower.

## Features:
* Different light settings.
* Temperature monitor.
* Soil sensor.

Thanks to [skiwithpete](https://www.youtube.com/channel/UCuwFJkahErfhbroefg12lzA)
for his videos on his RaspberryPi Home Automation project. A lot of inspiration
    on how to control the lights came from his videos!

    Thanks to [popoklopsi](http://popoklopsi.github.io/RaspberryPi-LedStrip/#!/)
    for his tutorial on controlling an RGB LED strip too!

## Parts List
All of these parts are the ones which were used when we built this. Some of them
are bought from eBay and the specific items may not be there any more, but you
can use any item that does the same job!

| Component | Quantity | Cost | Link/ Store |
| ---- | -------- | ---- | ----------- |
| Raspberry Pi 2 | 1 | £28.34 | https://www.element14.com/community/community/raspberry-pi |
| 8 Channel Relay Board | 1 | £6.79 | http://www.ebay.co.uk/itm/252051910091 |
| GU10 Light Socket | 10 | £6.19 | http://www.ebay.co.uk/itm/252214819333 |
| RGB LED Strip | 2x5m | £33.98 | http://www.amazon.co.uk/Waterproof-Multi-coloured-Controller-Decoration-Lighting/dp/B00CD2GZFM |
| 1 TO 1 Female 4 Pin Connector Extension Cable For RGB LED Strip | 2 | £1.98 | http://www.ebay.co.uk/itm/301442225669 |
| Connector Strip 15A | 10 | £6.14 | http://www.ebay.co.uk/itm/172158752476 |
| Red Wire | 10m | £2.79 | http://www.maplin.co.uk/p/maplin-equipment-wire-7-02mm-red-10m-bl07h |
| Black Wire | 10m | £2.79 | http://www.maplin.co.uk/p/maplin-equipment-wire-7-02mm-black-10m-bl00a |
| Container | 1 | £17.95 | http://www.amazon.co.uk/CrazyGadget%C2%AE-Garden-Storage-Container-Plastic/dp/B00ZDR650Y |
| Mylar (Highly Reflective Sheeting) | 5m | £14.95 | http://www.amazon.co.uk/Silver-Lightite-Strong-Reflective-Sheeting/dp/B01138AKSY |
| 3A Switch Mode UBEC 5V (Max 5A) | 1 | £2.91 | http://www.ebay.co.uk/itm/171533111781 |
| DS18B20 Digital Temperature Sensor | 1 | £1.46 | http://www.ebay.co.uk/itm/281196485870 |
| Soil Moisture Hygrometer Sensor | 1 | £2.79 | http://www.ebay.co.uk/itm/121588915786 |
| IRL540N N channel power mosfet | 6 | £6.46 | http://www.ebay.co.uk/itm/181298942866 |
| 12v PSU | 1 | £ |  |
| Breadboard | 1 | £ |  |
| WiFi Dongle | 1 | £ |  |
| xGB Micro SD Card | 1 | £ |  |




| Tool | Cost | Link/ Store |
| ---- | -------- | ---- | ----------- |
| Wire Stripper | £9.45 | http://www.ebay.co.uk/itm/390817438801 |
| Wire Cutter | £5.85 | http://www.ebay.co.uk/itm/231864549996 |

## To Do:
- [ ] Connect Relay to Pi & write code to control it.
- [ ] Connect 12V power to relay.
- [ ] Connect 1 bulb to relay.
- [ ] Connect 2 bulbs (in parallel) to relay.
- [ ] Connect 2 circuits of 2 bulbs to relay.
- [ ] Write more of to do list.

## Software Instructions
### Install Apache an
The first ting we will do is the software which allows us to control the raspberry pi pins through a nice web interface where we will have nice buttons to turn the lights on and off and change their colours, rather than typing commands all the time. A website is the best solution, it's compatible with all devices and you "only" need to know four languages: HTML (for the page's skeleton), CSS (page's style), PHP (interactions with the server) and JavaScript (interactions with the user).

We need to install a web server on the Raspberry Pi. We don't need a MySQL database, only a HTTP server and its PHP extension.
Update your Raspberry Pi with the "sudo apt-get update" command.
Install "sudo apt-get install apache2 php5 libapache2-mod-php5" to install Apache HTTP server and PHP5 extension.
Test if your server is working by typing the IP of your Raspberry Pi in your browser from any device which is connected to the same network. You should now see a "It works!" page. If you don't, then check your board's IP, try re-installing Apache or rebooting your Raspberry Pi. This page is showing that your Apache server is working properly, but we still need to test the PHP extension.
To check PHP extension "cd /var/www/html". "ls" command, you should have only one file named "index.html". This file is the "It works!" page. You can now delete it ("sudo rm index.html") and create another one called "index.php" (use "sudo nano index.php"). Then type the following text:

```php
<?php
    phpinfo();
    ?>
    ```
    After saving it `Ctrl + o`, exit nano `Ctrl + x`. Now if you refresh your browser, you should see a long page with lots of information about your server and PHP. If you don't, check the index.php file, try re-installing PHP or try to understand the error displayed instead of the page (Google it if necessary).

    Now do a git clone......
