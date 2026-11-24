# Renders the flat violet card background for the desktop widgets.
# No wallpaper is used: the widget window itself is made translucent (-alpha),
# so the real desktop shows through. Corners are the colour key.
param(
  [string]$Wallpaper, [int]$ScreenW, [int]$ScreenH,
  [int]$X, [int]$Y, [int]$W, [int]$H,
  [int]$Radius, [double]$Thick, [string]$Out,
  [int]$Key = 0x010101
)
Add-Type -AssemblyName System.Drawing
$ErrorActionPreference = "Stop"
$keyColor = [System.Drawing.Color]::FromArgb(255, ($Key -shr 16) -band 255, ($Key -shr 8) -band 255, $Key -band 255)
$bmp = New-Object System.Drawing.Bitmap $W, $H
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.Clear($keyColor)
$g.SmoothingMode = 'AntiAlias'; $g.PixelOffsetMode = 'HighQuality'
$d = $Radius * 2
$half = $Thick / 2.0
$rect = New-Object System.Drawing.RectangleF ([single]$half), ([single]$half), ([single]($W - $Thick)), ([single]($H - $Thick))
$path = New-Object System.Drawing.Drawing2D.GraphicsPath
$path.AddArc($rect.X, $rect.Y, $d, $d, 180, 90)
$path.AddArc($rect.Right - $d, $rect.Y, $d, $d, 270, 90)
$path.AddArc($rect.Right - $d, $rect.Bottom - $d, $d, $d, 0, 90)
$path.AddArc($rect.X, $rect.Bottom - $d, $d, $d, 90, 90)
$path.CloseFigure()
$fillRect = New-Object System.Drawing.RectangleF 0, 0, $W, $H
$top = [System.Drawing.Color]::FromArgb(255, 52, 38, 84)
$bot = [System.Drawing.Color]::FromArgb(255, 30, 20, 52)
$fill = New-Object System.Drawing.Drawing2D.LinearGradientBrush $fillRect, $top, $bot, 90.0
$g.FillPath($fill, $path)
$pen = New-Object System.Drawing.Pen ([System.Drawing.Color]::FromArgb(255, 150, 125, 205)), ([single]$Thick)
$g.DrawPath($pen, $path)
$g.Dispose()
$bmp.Save($Out, [System.Drawing.Imaging.ImageFormat]::Png)
