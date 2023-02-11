import bpy
from pathlib import Path
import subprocess

bl_info = {
	'name': 'Slicer STL Exporter',
	'blender': (2, 93, 0),
	'category': 'Object',
    "description": "Export selected object(s) as stls and open in slicer in a single click.",
    "author": "Greg Stretton",
    "version": (1, 0),
    "doc_url": "https://github.com/GKStretton/blender-slicer-stl-exporter"
}

PROPS = [
	('export_path', bpy.props.StringProperty(
		name='Export Path',
		description='Export path for stls behind the scenes',
		default='/tmp/stls',
		maxlen=20
	)),
	('slicer_executable', bpy.props.StringProperty(
		name='Slicer Executable',
		description='Command to run. stls will be appended to this to form final command',
		default='cura',
		maxlen=15
	)),
]

class ExportPanel(bpy.types.Panel):
	bl_idname = 'VIEW3D_PT_export_panel'
	bl_label = 'Slicer Exporter'
	bl_space_type = 'VIEW_3D'
	bl_region_type = 'UI'
	
	def draw(self, context):
		col = self.layout.column()
		for (prop_name, _) in PROPS:
			split = col.split(factor=0.5)
			col_label = split.column()
			col_label.label(text=prop_name)
			col_prop = split.column()
			col_prop.prop(context.scene, prop_name, text="") 
		col.operator('object.export_to_slicer', text='Export')

class ExportOperator(bpy.types.Operator):
	bl_idname = 'object.export_to_slicer'
	bl_label = 'Export Operator'
	bl_options = {'REGISTER'}
	
	def execute(self, context):
		scene = bpy.data.scenes["Scene"]
		context = bpy.context
		viewlayer = context.view_layer
		
		path = Path(scene.export_path)
		path.mkdir(parents=True, exist_ok=True)
		e = scene.slicer_executable

		obs = [o for o in context.selected_objects if o.type == 'MESH']
		bpy.ops.object.select_all(action='DESELECT')    

		slicerCommand = [e]

		for ob in obs:
			viewlayer.objects.active = ob
			ob.select_set(True)
			stl_path = path / f"{ob.name}.stl"
			slicerCommand.append(str(stl_path))
			bpy.ops.export_mesh.stl(
					filepath=str(stl_path),
					use_selection=True)
			ob.select_set(False)

		print(slicerCommand)
		subprocess.Popen(slicerCommand)
		return {'FINISHED'}

CLASSES = [
    ExportPanel,
    ExportOperator,
]

def register():
    print('registered') # just for debug
    
    for (prop_name, prop_value) in PROPS:
        setattr(bpy.types.Scene, prop_name, prop_value)
    
    for c in CLASSES:
        bpy.utils.register_class(c)
    
def unregister():
    print('unregistered') # just for debug
    
    for (prop_name, _) in PROPS:
        delattr(bpy.types.Scene, prop_name)
    
    for klass in CLASSES:
        bpy.utils.unregister_class(klass)
    

        
if __name__ == "__main__":
    register()