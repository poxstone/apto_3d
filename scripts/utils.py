import bpy, os, re

TABLE_INCH = [1.5, 0.6]
CHAR_SEPARATOR = '[_.]'
FLOAT_MAX_WIDTH = 2
FLOAT_MAX_LOCATION = 3
UNIDS = 100  # centimetro
#UNIDS = 1000  # milimetros
NAME_OBJ = {
    'MUEBLE': {
        'NAME_POSITION': 0,
        'mesinf':        'COCINA_PRINCIPAL',
        'messup':        'COCINA_SUPERIOR',
        'mesisl':        'COCINA_ISLA',
        'armbig':        'ARMARIO_GRANDE',
        'armsmall':      'ARMARIO_PEQUE',
    },
    'MATERIAL': {
        'NAME_POSITION': 1,
        'aglo':          'AGLOMERADO',
        'mdf':           'MDF',
    },
    'POSICION': {
        'NAME_POSITION': 2,
        'horizontal':   'HORIZONTAL',
        'verticafront': 'VERICAL_FRONTAL',
        'verticaback':  'VERICAL_POSTERIOR',
        'verticalat':   'VERICAL_LATERAL',
    },
    'COLOR': {
        'NAME_POSITION': 3,
        'claro':         'CLARO',
        'oscuro':        'OSCURO',
    },
    'VETA': {
        'NAME_POSITION': 4,
        'vetaN':        'NO_TIENE',
        'vetaA':        'ANCHO',
        'vetaL':        'LARGO',
    },
    'CANTO': {
        'NAME_POSITION': 5,
        'REGEX':        '^canto[0-4]([LA][1-4]?)?$',
        'L':            'LARGO',
        'A':            'ANCHO',
    },
    'NAME': {
        'NAME_POSITION': 6,
        'REGEX':        '^(pane|cajon|base)[A-Z]',
    },
    'CANTIDAD': {
        'NAME_POSITION': 7,
        'PREFIX':       'X',
        'REGEX':        '^X[0-9]{1,4}',
    },
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


def list_objects_csv(selection=None):
    selection = selection = auto_select(selection)
    result = 'mueble,name,material,color,ancho,largo,area,veta,canto,posicion,cantidad,x,y,z\n'
    for sel in selection:
        # to centimeters
        cantidad = 1
        position = ''
        area = ''
        material = ''
        color = ''
        mueble = ''
        canto = ''
        veta = ''
        ancho = ''
        largo = ''
        obj_name_arr = re.split(CHAR_SEPARATOR, sel.name)
        # get dimensions
        dim_x = round(sel.dimensions.x * UNIDS, FLOAT_MAX_WIDTH) if sel.dimensions.x else 0
        dim_y = round(sel.dimensions.y * UNIDS, FLOAT_MAX_WIDTH) if sel.dimensions.y else 0
        dim_z = round(sel.dimensions.z * UNIDS, FLOAT_MAX_WIDTH) if sel.dimensions.z else 0

        try:
            # cantidad
            if len(obj_name_arr) >= NAME_OBJ['CANTIDAD']['NAME_POSITION']:
                cantidad = obj_name_arr[NAME_OBJ['CANTIDAD']['NAME_POSITION']]
                if re.match(NAME_OBJ['CANTIDAD']['REGEX'], cantidad):
                    cantidad = int(cantidad.split(NAME_OBJ['CANTIDAD']['PREFIX'])[1])
                else:
                    cantidad = 1
            if int(cantidad) == 0:
                continue

            # is vertical or horizontal
            position = NAME_OBJ['POSICION'][obj_name_arr[
                                    NAME_OBJ['POSICION']['NAME_POSITION']]]
            # set material
            material = NAME_OBJ['MATERIAL'][obj_name_arr[
                                    NAME_OBJ['MATERIAL']['NAME_POSITION']]]
            # color
            color = NAME_OBJ['COLOR'][obj_name_arr[
                                    NAME_OBJ['COLOR']['NAME_POSITION']]]
            # mueble type
            mueble = NAME_OBJ['MUEBLE'][obj_name_arr[
                                    NAME_OBJ['MUEBLE']['NAME_POSITION']]]
            # veta
            veta = NAME_OBJ['VETA'][obj_name_arr[
                                    NAME_OBJ['VETA']['NAME_POSITION']]]
            # canto
            canto = obj_name_arr[NAME_OBJ['CANTO']['NAME_POSITION']]

            # set ancho y largo
            if position == NAME_OBJ['POSICION']['verticalat']:
                if dim_z > dim_y:
                    largo, ancho = dim_z, dim_y
                else:
                    largo, ancho = dim_y, dim_z
            elif position == NAME_OBJ['POSICION']['verticafront']:
                if dim_z > dim_x:
                    largo, ancho = dim_z, dim_x
                else:
                    largo, ancho = dim_x, dim_z
            elif position == NAME_OBJ['POSICION']['horizontal']:
                if dim_y > dim_x:
                    largo, ancho = dim_y, dim_x
                else:
                    largo, ancho = dim_x, dim_y
            
            # intercambia ancho para mantener las vetas en la tabla de corte final
            if veta == 'ANCHO':
                largo, ancho = ancho, largo

            # area
            area = round(largo*ancho, FLOAT_MAX_WIDTH) if ancho and largo else 0

            result += f"{mueble},{sel.name},{material},{color},{ancho},{largo},{area},{veta},{canto},{position},{cantidad},{dim_x},{dim_y},{dim_z}\n"
        except Exception as e:
            result += f"ERROR,{sel.name},{e}\n"

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
