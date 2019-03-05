# Fudge
A Powershell implant framework built on Python3/Flask- Designed for team collaboration and improved reporting.




### -- Upcoming Content --
#### Implant Manager

* Add password change
* Add Create user function
* Add icons to supplement text
* Order implant check-ins buy quality
* Set implant check-in colour to green/amber/red


##### Implant
* Create further staging options (docx, pfd, etc)
* Settings for Fudge boot


##### Controller
* Check for `fudge.db` in the working dir, if not configure new setup.
* Code refactor Controller to boot server & listener 
###  ----------------------



# Fudge Overview

## Setup
### Installation

The simplest route to get a basic Fudge server up and running is:

```
git clone https://github.com/Ziconius/Fudge
cd Fudge
pip3 install -r requirements.txt
sudo ptyhon3 Controller.py
```

Depending on your connections, you will likely need to configure a number of proxy and routing servers. The most common configuration and set up is to use Fudge with HTTPS using a reverse NGINX/Apache2 proxy.

## Login
After the inital installation you can log in with the default admin account using the credentiasl: `admin:letmein`. You will be prompted to the admin password as this point. 

## Users
Fudge comes with a default username and password, which prompts the user to change the password on first login

User configuration
to set up a new user log in with an admin account and select the new user option from the Global settings menu.

## Campaigns
#### What is a campaign?
A campaign is a method of organising a red team, which allows access control to be applies at a per user/per implant basis

Each campaign contains a unique name and, implants, and logs while a user can be a member of multiple campaigns



## Implants
#### What is an implant
An implant is the end result of sucessful stager. Ewach implant will have it's own stager, callback URL and ID. 

Creating a new implant will automatically configure new stagers, which relate to the implant.

#### Implant configuration
URL: An implant will be configured to call back to a given URL, or IP address.
Beacon time: [Default: 15 minutes] This is the time inbetween the implant calling back to the C2 server. Once an implant has been deployed it is possible to dynamically set this.
Protocols: A user will also need to select the protocols which the implant uses, the defaults are

* HTTP
* DNS 
* Binary protocol

A user can enable and disable protocols depending on the environment they believe they are working in.

Once an implant has been generated the Stagers page will provide a number of basic techniques which can be used to compromise the target. Currently stager techniques are as follows:

* IEX
* Windows Words Macro (In development)

