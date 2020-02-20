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