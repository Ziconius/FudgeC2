<p align="center">
  <img width="125" height="186" src="https://github.com/Ziconius/Fudge/blob/master/FudgeC2/ServerApp/static/fudge.png">
</p>

# FudgeC2
FudgeC2 is a Powershell command and control framework designed to facilitate team collaboration and campaign timelining, which aims to help clients better understand red team activities.

Built on Python3 with a web frontend, FudgeC2 aims to provide red teamers a simple interface in which to manage active implants across their campaigns.

_FudgeC2 is currently in beta, and should be used with caution in non-test environments. The beta was release at [BlackHat Arsenal USA 2019](https://www.blackhat.com/us-19/arsenal/schedule/#fudge-a-collaborative-c2-framework-for-purple-teaming-16968)._ 

## Setup
### Installation

To quickly install & run FudgeC2 on a Linux host run the following:

```
git clone https://github.com/Ziconius/FudgeC2
cd FudgeC2/FudgeC2
sudo pip3 install -r requirements.txt
sudo python3 Controller.py
```

For those who wish to use FudgeC2 via Docker, you can find the Docker [here](/Dockerfile). 

##### Settings:

FudgeC2' default server configurations can be found in the settings file:

`<install dir>/FudgeC2/Storage/settings.py`

These settings include FudgeC2 server application port, SSL configuration, and database name. For further details see the Server Configuration section.

N.b. Depending on your network design/RT architecture deployment, you will likely need to configure a number of proxy and routing adjustments.


#### First Login
After the initial installation you can log in with the default admin account using the credentials: 

```admin:letmein```

You will be prompted to the change the admin password after you login for the first time. 

### Server Settings

Certificates for any TLS are placed in the Storage directory, with the names placed within the settings.py file.

Port: This is the port number which the FudgeC2 server will bind to. The default is 5001.

DB name: The default name for the FudgeC2 database is ```fudge_c2.sql```. This can be altered if required.


## Users
Users within Fudge are divided into 2 groups, admins and standard users. Admins have all of the usual functionality, such as user and campaign creation, and are required to create a new campaigns.

Within campaign a users permissions can be configured to once of the following: None/Read/Read+Write. Without read permissions, a user will not be able to see the existence of a campaign, nor will they be able to read implant responses, or registered commands.

User with read permission will only be able to view the commands and their output, and the campaigns logging page. This role would typically be assigned to a junior tester, or an observer.

Users with write permissions will be able to create implant templates, and execute commands on all active implants.

_Note: in further development this will become more granular, allow write permissions on specific implants._

#### User Creation

An admin can create a new user from within the Global Settings options. They will also have the option to configure a user with admin privileges.


## Campaigns
#### What is a campaign?
A campaign is a method of organising a engagement against a client, which allows access control to be applied on a per user basis

Each campaign contains a unique name, implants, and logs while a user can be a member of multiple campaigns.


## Implants

Implants are broken down into 3 areas

* Implant Templates
* Stagers
* Active Implants

### Implant Templates
An implant template is the what we will create to generate our stagers. The implant template wil contain the default configuration for an implant. Once the stager has been triggered and an active implant is running on the host this can be changed.

The list of required configurations are:
* URL
* Initial callback delay
* Port
* Beacon delay
* Protocol:
  * HTTP (default)
  * HTTPS 
  * DNS
  * Binary
  
Once a template has been created the stager options will be displayed in the Campaign Stagers page.

### Stagers

The stagers are small scripts/macros etc which are responsible for downloaded and executing the full implant.

Once an implant has been generated the stagers page will provide a number of basic techniques which can be used to compromise the target. The stagers which are currently available are:

* IEX method
* Windows Words macro

### Built in commands
FudgeC2 has a variety of builtin functionality which can be invoked from the command input. The following commands can be executed on all FudgeC2 implants:

 - ```:: sys_info``` Collects username, hostname, domain, and local IP
 - ```:: enable_persistence``` Enables persistence by embedding a stager payload into the following autorun register key:
    - HKCU:\Software\Microsoft\Windows\CurrentVersion\Run\
 - ```:: export_clipboard``` Attempts to collect any text data stored in the users clipboard.
 - ```:: load_module [target script]``` This will load external powershell modules, such as JAWS.
 - ```:: exec_module [loaded module name]``` Executes a specific function of a loaded module.
 - ```:: list_modules``` Lists all loaded modules by the implant.

### Active Implants

Active implants are the result of successful stager executions. When a stager connects back to the Fudge C2 server a new active implant is generated, and delivered to the target host. Each stager execution & check-in creates a new active implant entry.


##### _Example_
As part of a campaign an user creates an implant template called "Moozle Implant" which is delivery to a HR department in via word macro. This then results in five successful execution of the macro stager; as a result the user will see five active implants.
 
 These will be listed on the campaigns main implant page, with a six character unique blob. The unique implants will be listed something similar to below:

```
Moozle Implant_123459
Moozle Implant_729151
Moozle Implant_182943
Moozle Implant_613516
Moozle Implant_810021
```

Each of these implants can be individually interacted with, or using the "ALL" keyword to register a command against all active implants.

### Implant communication

Implants will communicate back to the C2 server using whatever protocols the implant template was configured to use. If an implant is setup to use both HTTP and HTTPS, 2 listeners will be required to ensure that full commincation with the implant occurs.

Listeners are configured globally within Fudge from the Listeners page. Setting up and modifying the state of listeners requires admin rights, as changes to stagers may impact other on-going campaigns using the same Fudge server.

Currently the listeners page displays active listeners, but will allow admins to:
 - Create listeners for HTTP/S, DNS, or binary channels on customisable ports
 - Start created listeners
 - Stop active listeners
 - Assign common names to listeners

#### Implant configuration further info.
URL: An implant will be configured to call back to a given URL, or IP address.

Beacon time: [Default: 15 minutes] This is the time in between the implant calling back to the C2 server. Once an implant has been deployed it is possible to dynamically set this.

Protocols: The implant will be able to use of of the following protocols:
* HTTP
* DNS 
* Binary protocol

A user can enable and disable protocols depending on the environment they believe they are working in.


