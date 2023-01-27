import sys
sys.path.append("src/main/python")
from keycodes import *

KEYCODES_EXTRA_MODIFIERS = []

defined_modifiers = set()

# for k in KEYCODES_MODIFIERS:
    # defined_modifiers.add(k.code)

side_dict = {
    (MOD_LCTL ^ MOD_LCTL): "Left",
    (MOD_RCTL ^ MOD_LCTL): "Right"
}

modifier_dict = {
    MOD_LCTL: { "qmk": "CTL", "text": "Control" },
    MOD_LSFT: { "qmk": "SFT", "text": "Shift"   },
    MOD_LALT: { "qmk": "ALT", "text": "Alt"     },
    MOD_LGUI: { "qmk": "GUI", "text": "GUI"     }
}

modifier_combinations = range(MOD_LCTL, (MOD_LCTL | MOD_LSFT | MOD_LALT | MOD_LGUI) + 1)


def get_qmk_mod(side, modifiers, mod_mask, prefix = "", suffix = ""):
    return (prefix + side_dict[side][0] + modifier_dict[mod_mask]["qmk"] + suffix
            if modifiers & mod_mask
            else "")

def get_qmk_mods(side, modifiers):
    suffix = "|"
    qmk_mods = ""
    for mod in modifier_dict:
        qmk_mods += get_qmk_mod(side, modifiers, mod, "MOD_", suffix)
    return qmk_mods.rstrip(suffix)


def get_label_mod(modifiers, mod_mask):
    return (modifier_dict[mod_mask]["qmk"][0]
            if modifiers & mod_mask
            else "")

def get_label_mods(side, modifiers):
    label_mods = ""
    for mod in modifier_dict:
        label_mods += get_label_mod(modifiers, mod)
    return side_dict[side][0] + label_mods


def get_tooltip_mod(modifiers, mod_mask, suffix = ""):
    return (modifier_dict[mod_mask]["text"] + suffix
            if modifiers & mod_mask
            else "")

def get_tooltip_mods(side, modifiers):
    suffix = " + "
    tooltip_mods = ""
    for mod in modifier_dict:
        tooltip_mods += get_tooltip_mod(modifiers, mod, suffix)
    return side_dict[side] + " " + tooltip_mods.rstrip(suffix)


def print_key(key_code, qmk_code, label, tooltip, masked = True):
    print('    K(0x{:04X}, "{}", "{}", "{}", masked={}),'.
        format(key_code, qmk_code, label, tooltip, masked))


# Add missing One-Shot Modifiers
#
for side_mask in side_dict:
    for mod_mask in modifier_combinations:

        osm_code = QK_ONE_SHOT_MOD | side_mask | mod_mask

        if osm_code not in defined_modifiers:
            print_key(osm_code,
                      "OSM({})".format(get_qmk_mods(side_mask, mod_mask)),
                      "OSM\\n{}".format(get_label_mods(side_mask, mod_mask)),
                      "Enable {} for one keypress".format(get_tooltip_mods(side_mask, mod_mask)),
                      masked=False)

print()

# Add missing simple mods + key
#
for side_mask in side_dict:
    for mod_mask in modifier_combinations:

        mod_code = (side_mask | mod_mask) << 8

        if mod_code not in defined_modifiers:
            qmk_code = ""
            for mod in modifier_dict:
                qmk_code += get_qmk_mod(side_mask, mod_mask, mod, suffix = "(")
            qmk_code += "kc"
            for mod in modifier_dict:
                qmk_code += (")" if mod_mask & mod else "")

            print_key(mod_code,
                      qmk_code,
                      "{}\\n(kc)".format(get_label_mods(side_mask, mod_mask)),
                      get_tooltip_mods(side_mask, mod_mask) + " + kc")

print()

# Add missing Mod-Taps
#
for side_mask in side_dict:
    for mod_mask in modifier_combinations:

        mod_tap_code = MT(side_mask | mod_mask)

        if mod_tap_code not in defined_modifiers:
            print_key(mod_tap_code,
                      "MT({}, (kc))".format(get_qmk_mods(side_mask, mod_mask)),
                      "{}_T\\n(kc)".format(get_label_mods(side_mask, mod_mask)),
                      get_tooltip_mods(side_mask, mod_mask) + " when held, kc when tapped")
