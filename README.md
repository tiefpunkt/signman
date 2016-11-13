# SignMan - Digital Signage Manager

We had a bunch of flat screens at the Munich Maker Lab, but little use for them. So the all were put on the wall, and we decided to have them show random webpages and dashboards. However, configuring them all individually would have been a pain, so we needed something a little more automated. Cue the creation of SignMan.

SignMan allows you to manage a large group of screens and have them go through a list of websites, shown in full screen. The websites are managed and cued centrally, so all the screens need is a network connection.

In our setup, we use an OrangePi One board on each of the screens, running Armbian. They all connect to the SignMan server over HTTP, and then show one of the URLs we configured in the server component.

## Components
* [Server](server) - Server with WebUI to manage the screens
* [Client](client) - Client component run on the screen's computer boards
