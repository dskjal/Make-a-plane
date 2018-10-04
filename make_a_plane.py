# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####
import bpy, bmesh

bl_info = {
    "name" : "Make a plane",
    "author" : "dskjal",
    "version" : (1, 0),
    "blender" : (2, 79, 0),
    "location" : "View3D > Toolshelf > Make a plane",
    "description" : "Make a plane, moving a vertex in normal direction.",
    "warning" : "",
    "wiki_url" : "https://github.com/dskjal/Make-a-plane",
    "tracker_url" : "",
    "category" : "Mesh"
}

class MakeAPlaneButton(bpy.types.Operator):
    bl_idname = "dskjal.makeaplane"
    bl_label = "Make a plane"
    
    def execute(self, context):
        o = bpy.context.scene.objects.active
        if o.type != 'MESH' or o.mode != 'EDIT':
            raise TypeError('This addon workd in Edit mode on a mesh.')
            
        bm = bmesh.from_edit_mesh(o.data)
        if len(bm.select_history) < 4:
            raise Exception('Select 4 or more vertices.')

        # plane vertices, plane normal
        p1 = bm.verts[bm.select_history[0].index].co
        p2 = bm.verts[bm.select_history[1].index].co
        p3 = bm.verts[bm.select_history[2].index].co
        pn = (p1-p2).cross(p3-p1)

        for i in range(3, len(bm.select_history)):
            vert = bm.verts[bm.select_history[i].index]
            lp = vert.co
            ln = vert.normal
            vert.co = lp - ln * ( (pn.dot(lp - p1))/pn.dot(ln) )

        bmesh.update_edit_mesh(o.data)
        
        return {'FINISHED'}
        
class UI(bpy.types.Panel):
    bl_label = 'Make a plane'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Tools'
    
    @classmethod
    def poll(self, context):
        o = context.active_object
        return o and o.type == 'MESH' and o.mode == 'EDIT'
    
    def draw(self, context):
        self.layout.operator('dskjal.makeaplane')
        
def register():
    bpy.utils.register_class(MakeAPlaneButton)
    bpy.utils.register_class(UI)
    
def unregister():
    bpy.utils.unregister_class(UI)
    bpy.utils.unregister_class(MakeAPlaneButton)

if __name__ == "__main__":
    register()
