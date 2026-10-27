#!/usr/bin/env bash
# FX Linux — pre-KDE configuration preservation tool.
# Captures selected configuration only to OWNER-selected mounted FX11 data volume.
# No full-system image, no partition operations and no encryption requirements.
set -Eeuo pipefail
umask 077
export LC_ALL=C

usage() {
  cat <<'EOF'
FX Linux pre-KDE preservation

Usage:
  bash fx-linux-preserve.sh --dry-run /path/to/MOUNTED/FX11/FX-Linux-Config
  bash fx-linux-preserve.sh --capture /path/to/MOUNTED/FX11/FX-Linux-Config
  bash fx-linux-preserve.sh --verify /path/to/FX-LINUX-PRE-KDE-.../SHA256SUMS

The --capture operation writes ONLY to the specified backup destination.
It does not use sudo or change the source Linux installation.
NOTE: Selected FX Linux settings only. NOT an image or entire system backup.
OWNER chose the mounted FX11 partition as destination; no encryption is imposed.
The FX11 destination partition must NOT be formatted during Fedora KDE installation.
Do not upload resulting archives or reports to a public GitHub repository.
EOF
}

[[ $# == 2 ]] || { usage; exit 2; }
mode=$1
arg=$2
case "$mode" in --dry-run|--capture|--verify) ;; *) usage; exit 2 ;; esac

if [[ "$mode" == --verify ]]; then
  [[ -f "$arg" && "$(basename -- "$arg")" == "SHA256SUMS" ]] || { echo 'ERROR: specify an existing SHA256SUMS file' >&2; exit 2; }
  ( cd -- "$(dirname -- "$arg")" && sha256sum --check --strict SHA256SUMS )
  exit $?
fi

[[ ${EUID} -ne 0 ]] || { echo 'ERROR: run as normal Fedora user, NOT root/sudo' >&2; exit 2; }
[[ -d "$arg" ]] || { echo 'ERROR: destination directory does not exist; first mount FX11 and create the target folder.' >&2; exit 2; }
command -v findmnt >/dev/null || { echo 'ERROR: findmnt is required' >&2; exit 2; }
command -v tar >/dev/null || { echo 'ERROR: tar is required' >&2; exit 2; }
command -v sha256sum >/dev/null || { echo 'ERROR: sha256sum is required' >&2; exit 2; }

# Exact allowlist: Linux appearance, monitor, power, GRUB and FX tools only.
# Excludes entire HOME, browser profiles, Documents, SSH and generic app caches.
user_items=(
  .config/conky .conky .conkyrc .config/Conky
  .config/fenix-nightlight .local/share/fenix-nightlight .local/bin/fenix-nightlight
  .local/state/cosmic-comp/outputs.ron .local/state/cosmic-comp/outputs.ron.bak
  .config/cosmic .config/COSMIC
  .config/systemd/user .config/autostart
  .config/gtk-3.0/settings.ini .config/gtk-4.0/settings.ini
  .config/Kvantum .config/qt5ct .config/qt6ct
  .config/kdeglobals .config/kwinrc .config/plasmashellrc
  .config/plasma-org.kde.plasma.desktop-appletsrc .config/kscreen
  .local/share/icons .local/share/themes .local/share/wallpapers
  .icons .themes .gtkrc-2.0 .config/fontconfig
)
system_items=(
  etc/default/grub etc/default/grub.fxos-backup
  etc/systemd/logind.conf etc/systemd/logind.conf.d
  etc/systemd/sleep.conf.d etc/tuned
  etc/modprobe.d etc/sysctl.d etc/udev/rules.d
  etc/fstab etc/kernel/cmdline etc/dracut.conf.d
  boot/grub2/themes/fxos boot/loader/entries
)
user_found=() system_found=()
for p in "${user_items[@]}"; do [[ -e "$HOME/$p" || -L "$HOME/$p" ]] && user_found+=("$p"); done
for p in "${system_items[@]}"; do [[ -e "/$p" || -L "/$p" ]] && system_found+=("$p"); done

printf 'FX Linux pre-KDE CONFIG snapshot\nFound user paths: %s; system paths: %s\n' "${#user_found[@]}" "${#system_found[@]}"
printf '\nUser config paths to archive (relative to HOME):\n'
for p in "${user_found[@]}"; do printf '  %s\n' "$p"; done
printf '\nSystem paths to archive (relative to /):\n'
for p in "${system_found[@]}"; do printf '  %s\n' "$p"; done

if [[ "$mode" == --dry-run ]]; then
  printf '\nDRY RUN: no files copied. For capture choose a mounted, writable FX11 partition folder.\n'
  exit 0
fi

# Require a mounted filesystem separate from Fedora root. It may be a separate
# partition on the SAME physical disk, as explicitly chosen by OWNER.
# This alone cannot prove the partition will survive reinstall: verify lsblk.
root_mount=$(findmnt --noheadings --output TARGET --target / | head -n1)
dest_mount=$(findmnt --noheadings --output TARGET --target "$arg" | head -n1)
[[ -n "$dest_mount" && "$dest_mount" != "$root_mount" ]] || {
  echo 'ERROR: target must be an already mounted partition separate from the Fedora root filesystem.' >&2
  echo 'Mount the FX11 Windows volume and verify it using lsblk -f / findmnt.' >&2
  exit 2
}
[[ -w "$arg" ]] || { echo 'ERROR: destination is not writable.' >&2; exit 2; }

stamp=$(date -u +%Y%m%dT%H%M%SZ)
out="${arg%/}/FX-LINUX-PRE-KDE-${stamp}-$$"
mkdir -- "$out"
mkdir -- "$out/reports"
printf '%s\n' 'PRIVATE CONFIG ARCHIVE. MAY CONTAIN WIFI, PATHS, DEVICE DATA, LOCATION AND TOKENS.' \
  'Do not upload these archives or reports to GitHub. Keep privately in the selected FX11 folder.' \
  'This includes only selected FX Linux config and related technical reports, not an OS image or personal data.' \
  'Do not restore COSMIC session configuration into KDE wholesale.' > "$out/PRIVATE-README.txt"

# Tar keeps Linux metadata and symlinks within a portable archive even on NTFS.
# Do not extract COSMIC configs wholesale into the new KDE session.
failures=0
if (( ${#user_found[@]} )); then
  if ! tar -C "$HOME" -czf "$out/user-config.tar.gz" -- "${user_found[@]}" 2>"$out/reports/user-tar-errors.txt"; then
    echo 'WARNING: user archive reported errors; inspect reports/user-tar-errors.txt' >&2
    ((failures+=1))
  fi
fi
if (( ${#system_found[@]} )); then
  if ! tar -C / -czf "$out/system-config-readable.tar.gz" -- "${system_found[@]}" 2>"$out/reports/system-tar-errors.txt"; then
    echo 'WARNING: system archive has unreadable/changed items; inspect reports/system-tar-errors.txt' >&2
    ((failures+=1))
  fi
fi

# Capture commands are read-only. Their outputs may be personally identifiable.
run_report() {
  local title=$1; shift
  { printf '# %s\n' "$title"; "$@"; } > "$out/reports/$title.txt" 2>&1 || printf 'UNAVAILABLE OR ERROR: %s\n' "$title" >> "$out/reports/commands-with-errors.txt"
}
run_report os-release cat /etc/os-release
run_report kernel-version uname -r
run_report rpm-installed rpm -qa --qf '%{NAME}\t%{VERSION}-%{RELEASE}\t%{ARCH}\n'
run_report flatpak-installed flatpak list --app --columns=application,branch,origin
run_report dnf-repos dnf repolist --all
run_report user-enabled-units systemctl --user list-unit-files --state=enabled --no-pager
run_report system-enabled-units systemctl list-unit-files --state=enabled --no-pager
run_report current-power-profile powerprofilesctl get
run_report tuned-profile tuned-adm active
run_report swap swapon --show
run_report zram zramctl
run_report fs-mounts lsblk -o NAME,TYPE,FSTYPE,SIZE,MOUNTPOINTS
run_report root-mount findmnt --target /
run_report kernel-commandline cat /proc/cmdline
run_report grub-env grub2-editenv list

# Locate potential custom material outside normal paths without copying private
# Documents/Pictures or unknown application files. A human can decide what to add.
{
  echo '# Potential FX/Conky/theme files elsewhere in HOME (names only)'
  find "$HOME" -maxdepth 4 -type f \( -iname '*conky*' -o -iname '*fenix*' -o -iname '*fxos*' -o -iname '*fx-linux*' \) \
     -not -path '*/.cache/*' -not -path '*/.local/share/Trash/*' -print 2>/dev/null | head -n 200 || true
} > "$out/reports/possible-extra-files.txt"

{
  printf 'Capture timestamp UTC: %s\n' "$stamp"
  printf 'User tar paths: %s\n' "${#user_found[@]}"
  printf 'System tar paths: %s\n' "${#system_found[@]}"
  printf 'Tar creation failures: %s\n' "$failures"
  echo 'Checksum list excludes SHA256SUMS itself.'
  echo 'The selected FX11 partition is allowed on the same physical drive; DO NOT format it.'
} > "$out/reports/SUMMARY.txt"

( cd "$out" && find . -type f ! -name SHA256SUMS -print0 | sort -z | xargs -0 -r sha256sum > SHA256SUMS )
( cd "$out" && sha256sum --check --strict SHA256SUMS > "verification-result.txt" )
# verification-result is new output and must be covered by its own hash
( cd "$out" && sha256sum verification-result.txt >> SHA256SUMS && sha256sum --check --strict SHA256SUMS >/dev/null )

printf '\nBACKUP DIRECTORY: %s\n' "$out"
printf 'sha256: OK; tar errors: %s\n' "$failures"
printf 'Inspect reports/possible-extra-files.txt and both *tar-errors.txt files.\n'
printf 'Before reinstall: verify the FX11 partition will be preserved and identify the Fedora target partition.\n'
if (( failures > 0 )); then
  echo 'INCOMPLETE CONFIG ARCHIVE: review tar errors and recover inaccessible FX settings before reinstall.' >&2
  exit 1
fi
