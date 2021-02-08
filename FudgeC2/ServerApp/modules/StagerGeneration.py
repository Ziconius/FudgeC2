from Data.Database import Database
from NetworkProfiles.NetworkProfileManager import NetworkProfileManager

import ast


class StagerGeneration:
    # TODO: This needs cleaned up to ensure expandability with database changes.

    db = Database()
    NetProfMan = NetworkProfileManager()


    def generate_static_stagers(self, cid, user):
        ret_data = {}
        if self.db.campaign.Verify_UserCanAccessCampaign(user, cid):
            implant_info = self.db.implant.Get_AllImplantBaseFromCid(cid)
            if implant_info is not False:
                for implant in implant_info:

                    ret_data[implant['title']] = {
                        "description": implant['description'],
                        "url": implant['callback_url'],
                        "kill_date":implant['kill_date'],
                        "encryption":implant['encryption'],
                        "powershell_stager": self._generate_powershell_stager_string(implant),
                        "docm_macro_stager": self._generate_docx_stager_string(implant),
                        "stager_key": implant['stager_key'],
                        "operating_hours": implant['operating_hours']
                    }
            return ret_data
        else:
            return ret_data

    def GenerateSingleStagerFile(self, cid, user, stager_type):
        # TODO: Create docx file download from template.
        if self.db.campaign.Verify_UserCanAccessCampaign(user, cid):
            if stager_type == "docx":
                return self._generate_docx_stager_file()
            return
        else:
            return False

    def _generate_docx_stager_string(self, implant_data):
        stager_list = []
        if 'network_profiles' in implant_data:
            for element in implant_data['network_profiles']:
                raw = self.NetProfMan.get_docm_implant_stager(element, implant_data)
                if raw is not None:
                    stager_list.append(raw)
            return stager_list
        else:
            return stager_list

    def _generate_powershell_stager_string(self, implant_data):
        # Calls the Network Profile Manager to see if a powershell stager exists, if not the network profile will return
        #   a None value. Care should be taken to avoid comms which do not have any stager options to generate active
        #   payloads.
        stager_list = []
        if 'network_profiles' in implant_data:
            for element in implant_data['network_profiles']:
                raw = self.NetProfMan.get_powershell_implant_stager(element, implant_data)
                if raw is not None:
                    stager_list.append(raw)
            return stager_list
        else:
            return stager_list



'''
Get Stagers:

 - Types
 
 - Stager
 - Requires
 - Info
 
 
 


'''

