#!/usr/bin/env bash
# FenixSystem / Fedora KDE: derive network device from current default route.
# Output is Conky markup, not shell commands.
set -u
iface=""
if command -v ip >/dev/null 2>&1; then
  iface=$(ip -o -4 route show default 2>/dev/null | awk '{for(i=1;i<NF;i++) if ($i=="dev") {print $(i+1); exit}}')
  if [[ -z "$iface" ]]; then
    iface=$(ip -o -6 route show default 2>/dev/null | awk '{for(i=1;i<NF;i++) if ($i=="dev") {print $(i+1); exit}}')
  fi
fi
if [[ "$iface" =~ ^[a-zA-Z0-9_.:-]+$ ]]; then
  printf 'NET ↓ ${alignr}${downspeed %s}\nNET ↑ ${alignr}${upspeed %s}\n' "$iface" "$iface"
else
  printf 'NET ↓ ${alignr}--\nNET ↑ ${alignr}--\n'
fi
