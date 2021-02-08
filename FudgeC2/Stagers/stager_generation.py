from FudgeC2.Data.Database import Database

db = Database()

class StagerPowershellIEX:
    type = "string"
    requires = "http"
    name = "Powershell IEX"
    description = "Simple powershell IWR;IEX payload which requires a HTTP/S connection"

    def generate_payload(self):
        return "powershell.exe -c BLAH"

class StagerDocmMacroPayload:
    pass

class StagerGeneration:
    pass



    list_of_stagers = [
        StagerPowershellIEX
    ]


    def get_stager_options(self):
        # Return a list of stager options for a given implant template.

        result_object = {
            "type": None,
            "name": None,
            "description": None,

        }
        BLAH = []

        for stager in self.list_of_stagers:
            result_object['type'] = stager.type
            result_object['name'] = stager.name
            result_object['description'] = stager.description
            BLAH.append(result_object)

        return BLAH
