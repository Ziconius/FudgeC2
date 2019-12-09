class GetLoadedModules:
    type = "ML"
    args = None
    input = "list_modules"

    def process_implant_response(self):
        print("We're processing listed modules.")

    def implant_text(self):
        var = '''
function {{ ron.obf_get_loaded_modules }} () {
    $Script:tr = Get-Command | Where {$_.Source -Like "FC2"}
}
'''
        return var
