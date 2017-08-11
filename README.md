# saveWeaponHook

Hook `KeyValues::SetString(KeyValues *this, const char *s, const char *)` and save to log for crash tracing.

## Notice

linux platform only, and plugin generates log file `saveWeaponHook.log` in game root folder.