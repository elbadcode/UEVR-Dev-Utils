Most of these are half finished and maybe have some use cases that havent been fully explored. think of them as building blocks for your own code
Everything is free to use but let me know if you end up making something useful

# cleanupExclusions
remove most of the pointless shit that gathers in unrealvrmod folder

# dump.dll 
Universal plugin. press f8 objectarray to persistentdir in format needed for typeprinter  

# dumper-7.dll
Universal plugin. Fully featured dumper7 sdk generator. Better suited to creating standalone mods compared to uevr sdkdump. Generates mapping files for fmodel and ida function mappings. Also prints the same object dump format as above. Will almost certainly crash your game afterwards but this build is much more compatible than normal dumper7. Version is a few commits ahead but source is available at my dumper7uevr repo. Gamepad activation method added by markmon has been removed to prevent misclick. press f8 to activate 

# Install UEVR
get the newest nightly in one click! 

# type printer
sorts objects by type as separate files with the full asset path for each object per line. requires dump from either of the dump dlls

# aes.py
get aes keys for fmodel unpacking without having to visit a shady website directly

# logsaver.py
backup logs. was meant to also locate useful mem offsets and cache them but incomplete

# Cvar Differ
Definitely the most useful of the analysis scripts. Requires you to dump cvars from uevr. Run from your unrealvrmod dir. Will collect all common cvars and give aggregate data to identify the most common shared vars. For games with unique cvars you'll get a txt file listing them in the game profile dir

# sdkparse.py
incomplete and doesnt really have a clear goal but could be really useful for someone to build off of

# uevr_loader.addon64
piggyback off reshade (For loading only, doesnt fix reshade in vr but that is in progress). Load into any game you can load reshade in by hitting the reshade screenshot key. Requires a folder called UEVR with the backend and xr runtime dlls adjacent to the addon (so in the game dir most of the time). Reshade can load into basically every unreal game when named as d3d12.dll if dxgi.dll doesnt work or can be injected with lower chance of crashing. usually the internal load library hook is not detected so this is a very useful way to get into some games. Install reshade addon version from reshade.me
