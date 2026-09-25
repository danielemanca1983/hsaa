$ErrorActionPreference = 'Stop'
$sourceRoot = (Resolve-Path 'source-content').Path
$auditRoot = (Resolve-Path 'content-audit').Path
$app = New-Object -ComObject PowerPoint.Application
$app.AutomationSecurity = 3
$records = @()
try {
 foreach ($file in Get-ChildItem -LiteralPath $sourceRoot -Recurse -File | Where-Object { $_.Extension -in @('.ppt','.pptx') }) {
  $pres = $app.Presentations.Open($file.FullName,-1,0,0)
  try {
   foreach ($slide in $pres.Slides) {
    foreach ($link in $slide.Hyperlinks) {
     $records += @{ file=$file.Name; slide=$slide.SlideIndex; url=$link.Address; target=$link.SubAddress }
    }
    if ($file.Name -in @('Contacts & Supporters.ppt','John Larter Foundation.ppt')) {
     foreach ($shape in $slide.Shapes) {
      if ($shape.Type -in @(13,11)) {
       $prefix = if ($file.Name -eq 'Contacts & Supporters.ppt') {'supporter'} else {'foundation'}
       $name = "$prefix-$($slide.SlideIndex)-$($shape.Id).png"
       $shape.Export((Join-Path $auditRoot $name),2)
       $records += @{file=$file.Name; slide=$slide.SlideIndex; image=$name; left=$shape.Left; top=$shape.Top}
      }
     }
    }
   }
  } finally { $pres.Close() }
 }
} finally { $app.Quit() }
$records | ConvertTo-Json -Depth 5 | Set-Content (Join-Path $auditRoot 'slide-assets.json') -Encoding UTF8
Write-Output 'Extracted supplied hyperlinks and logos.'
