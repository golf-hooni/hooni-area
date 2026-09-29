# icons/*.svg 를 홈 화면용 PNG로 변환 (Edge 헤드리스 사용, 파이썬 이미지 라이브러리 불필요)
# 사용: powershell -File tools\render_icons.ps1   (hooni-area 폴더에서 실행)
$root = Split-Path $PSScriptRoot -Parent
$icons = Join-Path $root 'icons'
$edge = 'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'
$tmp = Join-Path $env:TEMP 'hooni-icons'
New-Item -ItemType Directory -Force $tmp | Out-Null
Copy-Item "$icons\icon-full.svg", "$icons\maskable.svg" $tmp
$jobs = @(@('icon-full.svg', 192, 'icon-192.png'), @('icon-full.svg', 512, 'icon-512.png'), @('maskable.svg', 512, 'maskable-512.png'))
foreach ($j in $jobs) {
  $name = [IO.Path]::GetFileNameWithoutExtension($j[2])
  $html = Join-Path $tmp "r_$name.html"
  Set-Content -Path $html -Encoding utf8 -Value ('<html><body style="margin:0;overflow:hidden;background:#FFF3D6"><img src="{0}" width="{1}" height="{1}" style="display:block"></body></html>' -f $j[0], $j[1])
  $out = Join-Path $icons $j[2]
  # 프로필 폴더를 매번 따로 써야 이전 결과가 재사용되지 않음
  $argList = @('--headless=new', '--disable-gpu', '--no-first-run', "--user-data-dir=$tmp\prof_$name", '--hide-scrollbars', '--force-device-scale-factor=1', "--window-size=$($j[1]),$($j[1])", "--screenshot=$out", ('file:///' + ($html -replace '\\', '/')))
  Start-Process -FilePath $edge -ArgumentList $argList -Wait -WindowStyle Hidden
  '{0}: {1} bytes' -f $j[2], (Get-Item $out).Length
}
