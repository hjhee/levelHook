# ../saveWeaponHook/saveWeaponHook.py
from .info import info
from listeners import OnLevelInit
import logging

import memory
from memory import Convention, DataType
from memory.hooks import PreHook
import memory.helpers
from memory.manager import TypeManager

secondaryWEaponName = [
    "baseball_bat",
    "cricket_bat",
    "crowbar",
    "electric_guitar",
    "fireaxe",
    "frying_pan",
    "golfclub",
    "katana",
    "knife",
    "machete",
    "riotshield", # won't show up in normal case
    "tonfa",
    "weapon_chainsaw",
    "weapon_pistol_magnum"
]

identifier_KeyValues_SetString = '_ZN9KeyValues9SetStringEPKcS1_'
map_cnt = 0

@OnLevelInit
def _on_level_init(map_name):
    global map_cnt
    logging.info('#{} map changed to {}.'.format(map_cnt, map_name))
    map_cnt += 1

def load():
    try:
        server = memory.find_binary('server')
    except:
        print('[saveWeaponHook] find binary server failed!')
        return

    logging.basicConfig(filename='saveWeaponHook.log', format='%(asctime)s %(levelname)s %(message)s')
    logging.info('plugin saveWeaponHook loaded.')

    UTIL_KeyValues_SetString = server[identifier_KeyValues_SetString].make_function(
        Convention.THISCALL,
        (DataType.POINTER, DataType.STRING, DataType.STRING), # KeyValues::SetString(KeyValues *this, const char *s, const char *)
        DataType.VOID
    )

    @PreHook(UTIL_KeyValues_SetString)
    def _pre_keyvalues_set_string(args):
        if args[1] == 'restoreSecondaryWeaponName':
            logging.info('setting restoreSecondaryWeaponName')
            args[2] = "weapon_pistol_magnum"
            return

            # args[2] may be not NUL-terminated
            value = memory.helpers.Array(TypeManager, false, "char", args[2], 20)
            
            weapon_name = args[2][:20] # not good enough

            logging.info('server_srv.so!KeyValues::SetString({}, {}).'.format(args[1], weapon_name))
            print('server_srv.so!KeyValues::SetString({}, {}).'.format(args[1], weapon_name))

            if not weapon_name in secondaryWEaponName:
                # sometimes value "weapon_chainsaw" occurres, could this crash the server?
                logging.info('invalid restoreSecondaryWeaponName: {}, set to {}'.format(weapon_name, "weapon_pistol_magnum"))
                print('invalid restoreSecondaryWeaponName: {}, set to {}'.format(weapon_name, "weapon_pistol_magnum")) # fallback value is "weapon_pistol_magnum"
                args[2] = "weapon_pistol_magnum"
