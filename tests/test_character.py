from utils.character import get_single_character_name, match_character


def test_match_character() -> None:
    # some basic matching
    assert match_character("mario") == ["<:mario:1290325306351288373>"]
    # more advanced
    assert match_character("incin, wii fit trainer, 4e") == [
        "<:incineroar:1290325020698087435>",
        "<:wiifittrainer:1290326138907918469>",
        "<:darksamus:1290324752447049881>",
    ]

    # matching one input to more than one char
    assert match_character("chroy, paisy") == [
        "<:roy:1290325851409350729>",
        "<:chrom:1290324662546464798>",
        "<:peach:1290325604289220669>",
        "<:daisy:1290324725612019773>",
    ]


def test_get_single_character_name() -> None:
    assert get_single_character_name("incin") == "incineroar"
    assert get_single_character_name("wii fit") == "wii fit trainer"
    assert get_single_character_name("4e") == "dark samus"
    assert get_single_character_name("mario") == "mario"
    assert get_single_character_name("chroy") == "roy"
    assert get_single_character_name("paisy") == "peach"
    assert get_single_character_name("squirtle") == "squirtle"
    assert get_single_character_name("ivysaur") == "ivysaur"
    assert get_single_character_name("charizard") == "charizard"
    assert get_single_character_name("pyra") == "pyra"
    assert get_single_character_name("mythra") == "mythra"
    assert get_single_character_name("11") == "captain falcon"
