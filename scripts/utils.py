import bpy, os, re

TABLE_INCH = [1.5, 0.6]
CHAR_SEPARATOR = '_'
FLOAT_MAX_WIDTH = 2
FLOAT_MAX_LOCATION = 3
UNIDS = 100  # centimetro
#UNIDS = 1000  # milimetros
MUEBLE = {
    'NAME_POSITION': 0,
    'mesinf':        'COCINA_PRINCIPAL',
    'messup':        'COCINA_SUPERIOR',
    'mesisl':        'COCINA_ISLA',
    'armbig':        'ARMARIO_GRANDE',
    'armsmall':      'ARMARIO_PEQUE',
}
COLOR = {
    'oscuro':'OSCURO',
    'claro':'CLARO',
}






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
    result = 'mueble,name,material,color,ancho,largo,area,veta,canto,posicion,x,y,z\n'
    for sel in selection:
        # to centimeters
        position = ''
        area = ''
        material = ''
        color = ''
        mueble = ''
        canto = ''
        veta = ''
        ancho = ''
        largo = ''
        obj_name_arr = sel.name.split(CHAR_SEPARATOR)
        # get dimensions
        dim_x = round(sel.dimensions.x * UNIDS, FLOAT_MAX_WIDTH) if sel.dimensions.x else 0
        dim_y = round(sel.dimensions.y * UNIDS, FLOAT_MAX_WIDTH) if sel.dimensions.y else 0
        dim_z = round(sel.dimensions.z * UNIDS, FLOAT_MAX_WIDTH) if sel.dimensions.z else 0

        # is vertical or horizontal
        if dim_x in TABLE_INCH:
            position = 'verticalat'
        elif dim_y in TABLE_INCH:
            position = 'verticafront'
        elif dim_z in TABLE_INCH:
            position = 'horizontal'

        # set material
        if 'aglo' in obj_name_arr:
            material = 'AGLOMERADO'
        elif 'mdf' in obj_name_arr:
            material = 'MDF'
        # color
        if 'oscuro' in obj_name_arr:
            color = 'OSCURO'
        elif 'claro' in obj_name_arr:
            color = 'CLARO'

        # mueble type
        mueble = MUEBLE[obj_name_arr[MUEBLE['NAME_POSITION']]]

        for indx in range(len(obj_name_arr)):
            # veta
            if re.match('^veta', obj_name_arr[indx]):
                veta_str = obj_name_arr[indx].replace('veta','')
                veta_arr = list(veta_str)
                if veta_arr[0] == 'N':
                    veta = f'NO'
                if veta_arr[0] == 'L':
                    veta = f'LARGO'
                if veta_arr[0] == 'A':
                    veta = f'ANCHO'

            # set ancho y largo
            if position == 'verticalat':
                if dim_z > dim_y:
                    largo = dim_z
                    ancho = dim_y
                else:
                    largo = dim_y
                    ancho = dim_z
            elif position == 'verticafront':
                if dim_z > dim_x:
                    largo = dim_z
                    ancho = dim_x
                else:
                    largo = dim_x
                    ancho = dim_z
            elif position == 'horizontal':
                if dim_y > dim_x:
                    largo = dim_y
                    ancho = dim_x
                else:
                    largo = dim_x
                    ancho = dim_y
            
            # canto
            if re.match('^canto', obj_name_arr[indx]):
                canto_str = obj_name_arr[indx].replace('canto','')
                canto_arr = list(canto_str)
                canto_total = canto_arr[0]
                canto_cmts = ''
                canto_priority = ''
                if len(canto_arr) >= 2:
                    if canto_arr[1] == 'L':
                        canto_priority = 'LARGO'
                    elif canto_arr[1] == 'A':
                        canto_priority = 'ANCHO'
                # calculate length
                if canto_total == 4:
                    canto_cmts = (largo * 2) + (ancho * 2)
                if canto_total == 3:
                    canto_cmts = (largo * 2) + (ancho * 2)
                
                #if len(canto_arr) >= 3:
                canto = f'cmts:{canto_total},{canto_cmts} - Prioridad{canto_priority}'
            
            # intercambia ancho para mantener las vetas en la tabla de corte final
            if veta == 'ANCHO':
                largo, ancho = ancho, largo

            # area
            area = round(largo*ancho, FLOAT_MAX_WIDTH) if ancho and largo else 0

        result += f"{mueble},{sel.name},{material},{color},{ancho},{largo},{area},{veta},{canto},{position},{dim_x},{dim_y},{dim_z}\n"
    return result

#to_print = list_objects_sizes()

def replace_name(original, sustitute, replace=True, selection=None):
    selection = selection = auto_select(selection)
    replaced = ''
    for sel in selection:
        original_name = sel.name
        if re.match(f'.*{original}.*', sel.name):
            if replace:
                sel.name = re.sub(original, sustitute, sel.name)
            replaced += f'{original_name},{sel.name},{original},{sustitute}\n'
    return replaced

#replace_name('canto_', 'canto')


def fix_positions_objects(positione=False,selection=None):
    selection = selection = auto_select(selection)
    changed = ''
    for sel in selection:
        changed += f'{sel.name},{sel.location}'
        if positione:
            sel.location.x = round(sel.location.x, FLOAT_MAX_LOCATION)
            sel.location.y = round(sel.location.y, FLOAT_MAX_LOCATION)
            sel.location.z = round(sel.location.z, FLOAT_MAX_LOCATION)
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
