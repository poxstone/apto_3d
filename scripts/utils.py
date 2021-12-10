import bpy, os

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
    

def return_objects_scaled(selection=None):
    selection = auto_select(selection)
    objects_scaled = ''
    for sel in selection:
        dim_str = []
        for scale in sel.scale:
            if not (scale == 1.0 or scale == -1.0):
                objects_scaled += f"{sel.name},{scale}\n"
                sel.select_set(True)
                continue
    return objects_scaled

#to_print = return_objects_scaled()


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
        if original in sel.name:
            if replace:
                sel.name = sel.name.replace(original, sustitute)
            replaced += f'{sel.name}, {original}, {sustitute}\n'
    return replaced

#replace_name('canto_', 'canto')


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
