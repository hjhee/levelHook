# levelHook

Hook `server_srv.so!PlayerSaveData::PlayerSaveData(CTerrorPlayer*, char const*)` and save to log for crash tracing.

## Notice

linux platform only, and plugin generates log file `levelHook.log` in game root folder.