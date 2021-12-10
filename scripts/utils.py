import bpy, os, re

TABLE_INCH = 1.5

def auto_select(selection=None):
    if selection == None:
        return bpy.data.objects
    elif type(selection) == str:
        try:
            return [bpy.data.objects[selection]]
        except:
            return []
    else:
        return bpy.context.selected_objects
    

def return_objects_scaled(reset_scale=False, selection=None):
    selection = auto_select(selection)
    objects_scaled = ''
    for sel in selection:
        dim_str = []
        for scale in sel.scale:
            if not (scale == 1.0 or scale == -1.0):
                objects_scaled += f"{sel.name},{scale}\n"
                sel.select_set(True)
                if reset_scale:
                    sel.scale.x = 1.0 if sel.scale.x > 0 else -1.0
                    sel.scale.y = 1.0 if sel.scale.y > 0 else -1.0
                    sel.scale.z = 1.0 if sel.scale.z > 0 else -1.0
                continue
    return objects_scaled

#to_print = return_objects_scaled(False)


def list_objects_sizes(selection=None):
    selection = selection = auto_select(selection)
    result = 'name,x,y,x,area\n'
    for sel in selection:
        dim_str = []
        cms2 = []
        for dim in sel.dimensions:
            dim_float = round(dim*100, 2)
            dim_str.append(str(dim_float))
            if not dim_float == TABLE_INCH:
                cms2.append(dim_float)
        result += f"{sel.name},{','.join(dim_str)},{round(cms2[0]*cms2[1],2)}\n"
    return result

#to_print = list_objects_sizes()

def replace_name(original, sustitute, replace=True, selection=None):
    selection = selection = auto_select(selection)
    replaced = ''
    for sel in selection:
        original_name = sel.name
        if re.match(original, sel.name):
            if replace:
                sel.name = re.sub(original, sustitute, sel.name)
            replaced += f'{sel.name},{original_name},{original},{sustitute}\n'
    return replaced

#replace_name('canto_', 'canto')


def fix_positions_objects(positione=False,selection=None):
    selection = selection = auto_select(selection)
    changed = ''
    for sel in selection:
        changed += f'{sel.name},{sel.location}'
        if positione:
            sel.location.x = round(sel.location.x, 3)
            sel.location.y = round(sel.location.y, 3)
            sel.location.z = round(sel.location.z, 3)
            changed += f',{sel.location}'
        changed += f'\n'
    return changed


# set path file
def export_file(content, file_name):
    tempFolder = os.path.dirname(bpy.data.filepath)
    file_path = os.path.join(tempFolder, '..', '..', 'csv_data', file_name)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    # save result into file
    file = open(file_path, "w")
    file.write(str(content))
    file.close()
    return file_path

#export_file(to_print, 'is_scaled.csv')
