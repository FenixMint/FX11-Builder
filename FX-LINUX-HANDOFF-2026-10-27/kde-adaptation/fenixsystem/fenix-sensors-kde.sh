#!/usr/bin/env bash
# FenixSystem / Fedora KDE: preserve output format and tolerate absent sensors.
set -u
read_hwmon() {
  local want="$1" input="$2" div="$3" decimals="$4"
  local path name raw
  for path in /sys/class/hwmon/hwmon*; do
    [[ -r "$path/name" && -r "$path/$input" ]] || continue
    IFS= read -r name < "$path/name" || continue
    [[ "$name" == "$want" ]] || continue
    IFS= read -r raw < "$path/$input" || continue
    [[ "$raw" =~ ^-?[0-9]+$ ]] || continue
    awk -v n="$raw" -v d="$div" -v places="$decimals" 'BEGIN {printf "%.*f",places,n/d}'
    return 0
  done
  printf '%s' '--'
}
cpu=$(read_hwmon k10temp temp1_input 1000 0)
gpu=$(read_hwmon amdgpu temp1_input 1000 0)
ssd=$(read_hwmon nvme temp1_input 1000 0)
fan=$(read_hwmon thinkpad fan1_input 1 0)
ppt=$(read_hwmon amdgpu power1_input 1000000 1)
printf 'CPU TEMP ${alignr}%s°C\nGPU TEMP ${alignr}%s°C\nSSD TEMP ${alignr}%s°C\nFAN ${alignr}%s RPM\nAPU PPT ${alignr}%s W\n' "$cpu" "$gpu" "$ssd" "$fan" "$ppt"
