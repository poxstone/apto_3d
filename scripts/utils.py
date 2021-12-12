import bpy, os, re

TABLE_INCH = [1.5, 0.6]
CHAR_SEPARATOR = '[_.]'
MILIMETERS = {
    'NAME': 'mm',
    'UNIDS': 1000,
    'FLOAT': 0,
}
CENTIMETERS = {
    'NAME': 'cm',
    'UNIDS': 100,
    'FLOAT': 2,
}
FLOAT_MAX_LOCATION = 3
UNIDS = MILIMETERS
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
        'verticalfront': 'VERICAL_FRONTAL',
        'verticalback':  'VERICAL_POSTERIOR',
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
        'REGEX':        '^canto([A][CON]){2}([L][CON]){2}$',
        'PREFIX':        'canto',
        'L':             'LARGO',
        'A':             'ANCHO',
        'O':             'OSCURO',
        'C':             'CLARO',
        'N':             'NINGUNO',
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


def list_objects_csv(show_errors=True, selection=None):
    selection = selection = auto_select(selection)
    unid = UNIDS["NAME"]
    result = f'mueble,name,abbr,material,color,ancho({unid}),largo({unid}),are({unid}),veta,canto,canto_len({unid}),posicion,cantidad,x({unid}),y({unid}),z({unid})'
    abbr_list = []
    for sel in selection:
        # to centimeters
        cantidad = 1
        abbr = ''
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
        dim_x = round(sel.dimensions.x * UNIDS['UNIDS'], UNIDS['FLOAT']) if sel.dimensions.x else 0
        dim_y = round(sel.dimensions.y * UNIDS['UNIDS'], UNIDS['FLOAT']) if sel.dimensions.y else 0
        dim_z = round(sel.dimensions.z * UNIDS['UNIDS'], UNIDS['FLOAT']) if sel.dimensions.z else 0

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
            # set ancho y largo
            if position == NAME_OBJ['POSICION']['verticalat']:
                if dim_z > dim_y:
                    largo, ancho = dim_z, dim_y
                else:
                    largo, ancho = dim_y, dim_z
            elif position == NAME_OBJ['POSICION']['verticalfront'] or position == NAME_OBJ['POSICION']['verticalback']:
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
            area = round(largo*ancho, UNIDS['FLOAT']) if ancho and largo else 0

            # canto
            canto_spell = obj_name_arr[NAME_OBJ['CANTO']['NAME_POSITION']].replace(NAME_OBJ['CANTO']['PREFIX'], '')
            # split each 2 char
            canto_arr = []
            for indx in range(0, len(canto_spell), 2):
                canto_arr.append(canto_spell[indx : indx + 2])
            canto_len = 0
            # calcule canto lenght
            for lad_grp in canto_arr:
                lad = lad_grp[0]
                col = lad_grp[1]
                if col == 'N':
                    continue
                long = ancho if lad == 'A' else largo
                canto_len += long
                canto += f"{NAME_OBJ['CANTO'][lad]}/{NAME_OBJ['CANTO'][col]}:{long};"

            # abbr
            name = obj_name_arr[NAME_OBJ['NAME']['NAME_POSITION']]
            abbr = f'{to_abbr(mueble,2)}_{to_abbr(color,1)}_{to_abbr(position,1)}_{to_abbr(name,2)}{len(abbr_list)}'
            abbr_list.append(abbr)
            # write row
            for i in range(cantidad):
                result += f"\n{mueble},{sel.name},{abbr},{material},{color},{ancho},{largo},{area},{veta},{canto},{canto_len},{position},1,{dim_x},{dim_y},{dim_z}"
        except Exception as e:
            if show_errors:
                result += f"\nERROR,{sel.name},{e}"

    return result

#to_print = list_objects_sizes()
def to_abbr(text, num_letters=1):
    abbr = ''
    t_arr = re.split('[_]', text)
    for tx in t_arr:
        abbr += tx[:num_letters].upper()
    return abbr


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
