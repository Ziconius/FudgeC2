#### Release Notes for 0.5.7:
New features:
 - SMTP support for notification and user account creation - further email notifications will be released in 0.5.8
 - RESTful API implementation created for the following functionality:
   - Campaign creation
   - SMTP/Email configuration
   - Implant interaction

Improvements/Changes:
 - UI changes to the campaign pages
 - Implants now display optional configurations, such as operating hours.
 - The implants default user agent now match Edge 44, and not Powershell/5.1
 - Dockerfile has been updated to pull from Kali Linux
 - User profile now contains more information

Documentation
 - Early OpenAPIv3 documentation (+ yaml) can be found at https://docs.moozle.wtf (Work in Progress)

Numerous bug fixes.

#### Release Notes for 0.5.6:

New features:
 - Optional payload encryption. This uses AES256 EAX with embedded keys.
 - Operating hours to control which times the implant is functioning.
 
Improvements
 - UI updates to improve the webapp visuals.
 - Updates to how command execution functions.
 - Improvements to setup during fresh installation.
 - Added error logging, which will be expanded for bug reporting.
 
Documentation
 - Added new Docker repo for major releases.
 - Added docker compose file.

Bug fixes
 - Download file now correctly notifies the user of an error if the download fail
 - Other misc fixes

#### 0.5.5 Changes
 _*N.b This version of FudgeC2 will not function with older versions*_
 
 - Added screenshot modules
 - Added screenshot modal to display larger images

Active Implant selection page now highlight the implant text to make finding living implants easier
Reworked appearance of the commands awaiting section to improve their presentation.
Improvements to handling data types in the database. This is a DB breaking change!
Removed output from persistence mechanism in the powershell terminal

Code improvements to builtin commands to allow checking of submitted arguments, i.e. checking for local files before attempting to upload them (File uploads, module loads, playing audio), or checking for dangerous commands.

Play_audio module updates:
 - Now plays wav files instead of mp3.
 - No longer writes temp files to disk, uses MemoryStream to remain off disk
 - Utilises the command argument checks to ensure the wav files exists before registering the command on the C2

Refactored sections of the code base are responsible for generating the strings used to communicate with the implant, and which are used to generate the implant core execution string. This makes creating modules, and network profiles simplier to understand.

#### 0.5.4 Changes

Added HTTPS listener which currently mirrors BasicHttpProfile, except via TLS and endpoint changes.

Refactoring how command registration takes place.

Refactor obfuscation levels implement proper checking

Improved stager listener/stability since network profile changes

Bug fix: Start/stopping listeners now occurs properly

Misc other fixes.


#### 0.5.3 Changes
Listeners have been removed and replaced with a much more flexible design now referred to as Network Profiles. These are created from three files:
 - Network profile
 - Profile interface
 - Profile listener

Network Profiles which can be built by anyone to create custom communication protocols, or tweak existing profiles.

Each profile is responsible for populating several pages within Fudge C2. There have been numerous change in this revision of FudgeC2 ready for the upcoming release of 2 network profiles. For more information see the FudgeC2 wiki for more information on how to build a network profile.

Network Profiles now control the following:
 - Network Profiles are now used to populate and validate the implant template
 - New listeners can be created from the available network profiles
 - Stager page has been updated, it now displayed a stagers per network profile.