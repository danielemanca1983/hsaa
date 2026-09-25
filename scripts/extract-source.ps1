$ErrorActionPreference = 'Stop'
$sourceRoot = (Resolve-Path 'source-content').Path
$auditRoot = Join-Path (Get-Location).Path 'content-audit'
New-Item -ItemType Directory -Force -Path $auditRoot | Out-Null
$records = [System.Collections.Generic.List[object]]::new()
$wordApp = New-Object -ComObject Word.Application
$wordApp.Visible = $false
$wordApp.DisplayAlerts = 0
$wordApp.AutomationSecurity = 3
try {
 foreach ($file in Get-ChildItem -LiteralPath $sourceRoot -Recurse -File -Filter '*.doc') {
  if ($file.Name -match 'LOG IN') { continue }
  $document = $wordApp.Documents.Open($file.FullName, $false, $true, $false)
  try {
   $tables = @()
   foreach ($table in $document.Tables) {
    $rows = @()
    foreach ($row in $table.Rows) {
     $cells = @()
     foreach ($cell in $row.Cells) { $cells += $cell.Range.Text.Trim([char]13,[char]7) }
     $rows += ,$cells
    }
    $tables += ,$rows
   }
   $links = @($document.Hyperlinks | ForEach-Object { @{ text=$_.TextToDisplay; url=$_.Address } })
   $records.Add(@{file=$file.FullName.Substring($sourceRoot.Length+1); type='word'; text=$document.Content.Text; tables=$tables; links=$links})
  } finally { $document.Close(0) }
 }
} finally { $wordApp.Quit() }
$powerpointApp = New-Object -ComObject PowerPoint.Application
$powerpointApp.AutomationSecurity = 3
try {
 $index = 0
 foreach ($file in Get-ChildItem -LiteralPath $sourceRoot -Recurse -File | Where-Object { $_.Extension -in @('.ppt','.pptx') }) {
  $index++
  $presentation = $powerpointApp.Presentations.Open($file.FullName, -1, 0, 0)
  try {
   $slides = @()
   foreach ($slide in $presentation.Slides) {
    $texts = @()
    foreach ($shape in $slide.Shapes) {
     if ($shape.HasTextFrame -and $shape.TextFrame.HasText) { $texts += $shape.TextFrame.TextRange.Text }
     if ($shape.HasTable) {
      foreach ($row in $shape.Table.Rows) {
       foreach ($cell in $row.Cells) { $texts += $cell.Shape.TextFrame.TextRange.Text }
      }
     }
    }
    $render = "deck-$index-slide-$($slide.SlideIndex).jpg"
    $slide.Export((Join-Path $auditRoot $render), 'JPG', 1600, 900)
    $slides += @{number=$slide.SlideIndex; text=$texts; render=$render}
   }
   $records.Add(@{file=$file.FullName.Substring($sourceRoot.Length+1); type='powerpoint'; slides=$slides})
  } finally { $presentation.Close() }
 }
} finally { $powerpointApp.Quit() }
$records | ConvertTo-Json -Depth 12 | Set-Content -LiteralPath (Join-Path $auditRoot 'extracted.json') -Encoding UTF8
Write-Output "Extracted $($records.Count) public-content documents into content-audit. Credential document excluded."
