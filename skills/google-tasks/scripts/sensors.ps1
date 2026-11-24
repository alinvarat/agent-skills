# Streams one JSON line every few seconds for tasks_widget.py:
#   {"ac":true,"bat":100,"dis_w":null,"chg_w":null,"cpu_t":57.9,"cpu":12.3,"gpu":3.1}
# cpu_t = ACPI thermal zone (Kelvin->C), cpu = total CPU utility %, gpu = 3D engine utilisation %.
# Exits by itself when the parent widget process is gone.
param([int]$ParentPid = 0, [int]$Interval = 3)
$ErrorActionPreference = "SilentlyContinue"
$counters = @(
  '\Thermal Zone Information(*)\Temperature',
  '\Processor Information(_Total)\% Processor Utility',
  '\GPU Engine(*engtype_3D)\Utilization Percentage'
)
Get-Counter -Counter $counters -SampleInterval $Interval -Continuous | ForEach-Object {
  if ($ParentPid -gt 0 -and -not (Get-Process -Id $ParentPid)) { exit }
  $t = $null; $cpu = $null; $gpu = 0.0
  foreach ($s in $_.CounterSamples) {
    $p = $s.Path
    if ($p -like '*thermal zone information*temperature') { if ($null -eq $t -or $s.CookedValue -gt $t) { $t = $s.CookedValue } }
    elseif ($p -like '*processor utility*') { $cpu = $s.CookedValue }
    elseif ($p -like '*gpu engine*') { $gpu += $s.CookedValue }
  }
  $bs = Get-CimInstance -Namespace root/wmi -ClassName BatteryStatus | Select-Object -First 1
  $bat = Get-CimInstance Win32_Battery | Select-Object -First 1
  $dis = $null; $chg = $null
  if ($bs) {
    if ($bs.Discharging -and $bs.DischargeRate -gt 0) { $dis = [math]::Round($bs.DischargeRate / 1000.0, 1) }
    if ($bs.Charging -and $bs.ChargeRate -gt 0) { $chg = [math]::Round($bs.ChargeRate / 1000.0, 1) }
  }
  $o = [ordered]@{
    ac    = if ($bs) { [bool]$bs.PowerOnline } else { $null }
    bat   = if ($bat) { $bat.EstimatedChargeRemaining } else { $null }
    dis_w = $dis
    chg_w = $chg
    cpu_t = if ($null -ne $t) { [math]::Round($t - 273.15, 1) } else { $null }
    cpu   = if ($null -ne $cpu) { [math]::Round([math]::Min($cpu, 100), 1) } else { $null }
    gpu   = [math]::Round([math]::Min($gpu, 100), 1)
  }
  [Console]::Out.WriteLine(($o | ConvertTo-Json -Compress))
  [Console]::Out.Flush()
}
