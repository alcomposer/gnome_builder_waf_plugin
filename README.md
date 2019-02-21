# Gnome-Builder Waf Plugin

This project is to allow the building of Waf projects using Gnome Builder. Specifically for the Ardour project. 

Currently it can:
* Configure
* Build 
* Clean

https://wiki.gnome.org/Apps/Builder

https://www.ardour.org

https://waf.io/

# Use:
Place both `waf_plugin.py` & `waf_plugin.plugin` into `~/.local/share/gnome-builder/plugins`. If the directory does not exist create it.
Tested on Arch Linux, Gnome-Builder Nightly, (3.31.9) 

# Current Issues:
* The plugin needs Gnome-Builder Nightly due to using `SimpleBuildSystemDiscovery`, which IIRC is not preset in older Builder versions.
* Currently, Python2 is hard-coded (probably best to change this)

# Future work:
 * It is inteded that Gnome-Builder will allow reading of **clang** `compile_commands.json` from within python in the future, and as such this plugin will read pass that information into Gnome-Builder.
 * Projects that use Gnome-Builder with this plugin in future will need to include: `clang_compiliation_database.py` in their `wscript` in order to use code completion / search inside Builder
 
# Waf Clang Compilation Database info:
Add `clang_compilation_database.py` inside root directoy of Waf project (if not already built into the projects `waf` archive, and call it within the `wscript` like so:
```python
def configure(conf):
        conf.load('compiler_cxx')
        ...
        conf.load('clang_compilation_database')
```
(above information & link for `clang_compiliation_database.py`)
https://gitlab.com/ita1024/waf/blob/master/waflib/extras/clang_compilation_database.py
