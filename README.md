# Fudge
A Powershell implant framework built on Python3/Flask- Designed for team collaboration and improved reporting.




### -- Upcoming Content --
#### Implant Manager
* Add password change on first login. 
  * Add first login value in DB + schema
  * Update schema to reflect a new build
* Add bcrypting on passwords
* Add password change
* Add Create user function

##### Controller
* Check for `fudge.db` in the working dir, if not configure new setup.
###  ----------------------


# Fudge Overview
## Users
Fudge comes with a default username and password, which prompts the user to change the password on first login

User configuration


## Campaigns
#### What is a campaign?
A campaign is a method of organising a red team, which allows access control to be applies at a per user/per implant basis

Each campaign contains a unique name and, implants, and logs while a user can be a member of multiple campaigns



##Implants
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

A user can enable and disable depending on their requirements
