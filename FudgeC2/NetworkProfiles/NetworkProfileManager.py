from NetworkProfiles.Profiles.BasicHttpProfile.BasicHttpProfile import BasicHttpProfile
from NetworkProfiles.Profiles.HttpsProfile.HttpsProfile import HttpsProfile


class NetworkProfileManager:
    # Add new Network Profiles to the profiles list. Profiles must be compliant to
    #   the standards to be functional w/o the risk of error.
    profiles = [
        BasicHttpProfile(),
        HttpsProfile()
        # Current profiles in dev branches:
        # TcpProfile()
        # HttpsProfile()
        # DnsProfile()
        # EncryptedHttpProfile()
    ]

    def get_available_profiles(self):
        avaliable_profiles = []
        for netprof in self.profiles:
            avaliable_profiles.append(netprof.name)
        return avaliable_profiles

    def get_implant_powershell_code(self, profile_tag):
        for netprof in self.profiles:
            if profile_tag == netprof.profile_tag:
                return netprof.get_powershell_code(), netprof.get_powershell_obf_strings()
        return False

    def get_implant_template_code(self):
        code = []
        for x in self.profiles:
            code.append(x.get_webform())
        return code

    def validate_web_form(self, key, value):
        for x in self.profiles:
            if key == x.profile_tag:
                a = x.validate_web_form(key, value)
                return a
        return False

    def get_powershell_implant_stager(self, profile_tag, implant_data):
        for profile in self.profiles:
            if profile.profile_tag == profile_tag:
                return profile.get_powershell_implant_stager(implant_data)

    def get_docm_implant_stager(self, profile_tag, implant_data):
        for profile in self.profiles:
            if profile.profile_tag == profile_tag:
                return profile.get_docm_implant_stager(implant_data)

    def get_all_listener_forms(self):
        a = []
        for x in self.profiles:
            a.append(x.get_listener_profile_form())
        return a

    def get_listener_interface(self, profile_tag):
        print(f"get_listener_interface(){profile_tag}")
        for x in self.profiles:
            if x.profile_tag == profile_tag:
                return x.get_listener_interface()
        print(f"Error: get_listener_interface(){profile_tag}")

    def get_listener_object(self, profile_tag):
        for x in self.profiles:
            if x.profile_tag == profile_tag:
                return x.get_listener_object()
