# Blender Slicer STL Exporter

> Export selected objects in Blender to Cura or your chosen slicer in a single click

This is a simple addon that supports easy export of objects to your chosen slicer.

Once enabled, the addon is found under the "Misc" section of the right-hand side
viewport menu (toggled with 'n').

## Usage

- export_path: the location where stls get exported. You don't need to interact with this usually because they automatically get opened in the slicer. e.g. /tmp/stls
- slicer_executable: the command to run to open the slicer. e.g. cura

This supports exporting multiple objects at once. They will be individually exported as stls and then opened by the slicer. The slicer command is formed like so for 2 objects Cube and Cylinder (auto-exported with .stl suffix):

```bash
[slicer_executable] [export_path]/Cube.stl [export_path]/Cylinder.stl
```

Tested with Cura, not tested with any other slicers.

## Recommendations

This automates Blender -> Slicer, but there's also lots of automation potential from slicer -> printer. Octoprint can be used for remote printing. Cura can export straight to Octoprint after slicing. There are many octoprint plugins, including smart plug control so that the printer automatically turns on after an upload. Therefore with a bit of setup the whole workflow can be reduced to the following:

1. select object in blender
2. Click "export" from the above addon
3. Click "slice" in Cura 
4. Click "upload to Octoprint"
5. ...printer automatically turns on and prints.