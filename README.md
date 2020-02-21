<p align="center">
  <img width="125" height="186" src="https://github.com/Ziconius/Fudge/blob/master/FudgeC2/ServerApp/static/images/fudge.png">
</p>


# FudgeC2
[![Commit Activity](https://img.shields.io/github/commit-activity/m/ziconius/fudgec2)](https://github.com/ziconius/FudgeC2/graphs/commit-activity)
[![Code Quality](https://img.shields.io/codeclimate/maintainability-percentage/Ziconius/FudgeC2)](https://codeclimate.com/github/Ziconius/FudgeC2)
[![Licence](https://img.shields.io/github/license/ziconius/fudgec2)](https://github.com/ziconius/FudgeC2/blob/master/LICENSE.txt)
[![Stars](https://img.shields.io/github/stars/ziconius/fudgec2)](https://github.com/Ziconius/FudgeC2/stargazers)


FudgeC2 is a Powershell C2 platform designed to facilitate team collaboration and campaign timelining, released at [BlackHat Arsenal USA 2019](https://www.blackhat.com/us-19/arsenal/schedule/index.html#fudge-a-collaborative-c-framework-for-purple-teaming-16968). This aims to help clients better understand red team activities by presenting them with more granular detail of adversarial techniques.

Built on Python3 with a web frontend, FudgeC2 aims to provide red team operators a simple interface in which to manage active implants across their campaigns.

_FudgeC2 is in active development, and is receiving regular updates - if you have feature suggestions reach out with your ideas and suggestions._

### Installation

To install and configure FudgeC2 run the following:

```
git clone https://github.com/Ziconius/FudgeC2
cd FudgeC2/FudgeC2
sudo pip3 install -r requirements.txt
sudo python3 Controller.py
```
This will generate the F2 database, and first time credentials. You will then be able to access the platform from *http[s]://127.0.0.1:5001/*. The logon credentials are:

`admin`:`letmein`

For more information on installation and configuration see the wiki, [here](https://github.com/Ziconius/FudgeC2/wiki/Installation-and-Setup).

### Implant Builtin Functionality

FudgeC2 breaks projects down into campaigns. Each campaign will have their own implant templates, active implants, users, and targets.

To start you simply need to generate a new campaign, create an implant template with the campaign, and trigger one of the stagers on a target computer.

![fudgec2_implant_example](https://user-images.githubusercontent.com/6460785/75062098-09120100-54da-11ea-8b56-25f359c04535.png)

F2 implants contain a variety of builtin commands, which are also easily extended upon allowing operators the chance to create their own builtin functionality. An overview of functionality can be seen below, for more information on the builtin implant functionality or how to create custom modules see FudgeC2s' wiki, [found here](https://github.com/Ziconius/FudgeC2/wiki/Implant-Functionality).

**Implant functionality**

|Command        | Info
|-------        |-----
| `<command>`               |If no builtin prefix  in used the submitted value will be directly executed by Powershell.|
|`:: sys_info`              | Collects username, hostname, domain, and local IP
|`:: enable_persistence`    | Enables persistence by embedding a stager payload into the following autorun registry key
|`:: export_clipboard`      | Attempts to collect any text data stored in the users clipboard.
|`:: load_module [target script]` |This will load external powershell modules, such as JAWS.
|`:: exec_module [loaded module name]` |Executes a specific function of a loaded module.
|`:: list_modules`          |Lists all loaded modules by the implant.
|`:: download_file [target file]`  |Downloads the target file to the FudgeC2 server
|`:: upload_file [local file] [remote path/filename]`  |Uploads a file to the target path and specific filename
|`:: play_audio [audio file (WAV)]`  |Plays a WAV audio file on the compromised host.
|`:: screenshot`  |Takes a screenshot of the compromised hosts desktop.



![fudgec2_implant_example](https://user-images.githubusercontent.com/6460785/75062098-09120100-54da-11ea-8b56-25f359c04535.png)


### Contributing
All contributions, suggestions, and feature requests are welcome. Feel free to reach out over GitHub, or via [Twitter](https://twitter.com/Ziconius) with ideas, suggestions and questions.


### License
The FudgeC2 project and all module are under the GNU General Public License v3.0 unless explicitly noted otherwise. You can find the full licence [here](/LICENCE.txt)