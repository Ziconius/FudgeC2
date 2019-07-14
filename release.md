## Active Development
Below is an high-level overview of the on-going development to increase functionality, and reliability of Fudge. This is broken down into release cycles, which are focused around core functionality changes.

---
**Release 0.5 _(Goblin Sapper)_**

Create further obfuscation and jinja templatework
 C2 Server
 - [ ] Add function name randomisation for all functions
 - [ ] Create protocol obfuscation
 - [ ] Add comments and contact details into unobfuscated implant
 Web App
 - [ ] Add text/comments for unobfuscated implant

---
**Release 0.6 _(Worgen Shaman)_**

Review and improve all database content & create export functionality
 - [ ] Define what data should be exported and sent to clients
 - [ ] Build suitable encryption
 - [ ] Anonymize campaign usernames
 
Web App
 - [ ] Export should allow user submitted password
 - [ ] Download should be a single file
 - [ ] Review possible options which maybe required when downloading? I.e data exclusion
 
 
---
**Release 0.7 _(Undead Alchemist)_**

Create export viewer
 - [ ] _Actions undefined at this stage_

---
**Release 0.8 _(Unnamed)_**

Create DNS listener
- [ ] _Actions undefined at this stage_
 
---
**Release 0.9 _(Unnamed)_**

Further implement builtin keywords implants
- [ ] _Actions undefined at this stage_

---
**Release 1.0 _(Unnamed)_**

Review and improve web application performance and output
- [ ] _Actions undefined at this stage_
- [ ] Provide feedback if listener channel is in use, or not running when creating an implant



---
## Released Versions
Below is a list of all versions which are now tagged with release, and can be found:

---
**Release 0.4 _(Tauren Herbalist)_**

Review how data is captured from listeners and webapp
 - [x] Improve logging across web application
 - [x] Add user action logs
 - [x] Review Database.py and create common format for readability and maintainability
 - [x] Add check to look for latest version of FudgeC2 - Notify user of updates.

---
Release 0.3 _(Dwarven Blacksmith)_
Release cross-protocol implant communications using HTTP/HTTPS

C2 Server:
 - [x] Capture and log returning protocol
 - [x] Add certificate/key path and name into options
 - [x] Improve error checking + logging
 
Web App:
 - [x] Allow multiple protocols + port to be selected
 
Implant 
 - [x] Implement random protocol selection for callback
 - [x] Ensure C2 certificates are present
 - [x] Implement function/variable name randomisation in implant
 

---
Release 0.2 _(Human Grunt)_ **Released**
#### Implant Manager Web App
- [x] Add help page with implant special tags using `::cmd::` format.
- [x] Order implant check-in by time
- [x] Review how implant responses are displayed within the main campaign page to improve readability.
- [x] Create log page with detailed logging of for each implant, including time, command, implant, pickup, and pickup time.
- [x] Provide feedback to read-only campaign users with feedback if they are not authorised to execute commands. Basic implementation only.
- [x] Improve Campaign Settings radio buttons to display the current configuration.


##### Implant


- [x] Add implant special tags formatted: `::cmd::`
- [x] Create further staging options (docm)
- [x] Improve format of returning data.
- [x] Deploy HTTPS listener
    - [x] Allow C2 to run on untrusted cert. (Deploying own certs instead - untrusted cannot be used.)

##### Controller
- [x] Check for `fudge.db` in the working dir, if not configure new setup. 
- [x] Code refactor Controller to boot server & listener 
- [x] Clean code for version release - partial

 
 ---