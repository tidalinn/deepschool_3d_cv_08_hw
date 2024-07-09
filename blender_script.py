import bpy
import bpy_extras.object_utils
import math


def save_bbox(camera, scene, object):
    matrix = object.matrix_world
    mesh = object.bound_box

    col_0 = matrix.col[0]
    col_1 = matrix.col[1]
    col_2 = matrix.col[2]
    col_3 = matrix.col[3]

    min_x = 1
    max_x = 0
    min_y = 1
    max_y = 0

    for t in range(0, len(mesh)):
        co = mesh[t]
        pos = (col_0 * co[0]) + (col_1 * co[1]) + (col_2 * co[2]) + col_3
        pos = bpy_extras.object_utils.world_to_camera_view(scene, camera, pos)
    
        if (pos.x < min_x):
            min_x = pos.x
        if (pos.y < min_y):
            min_y = pos.y
        if (pos.x > max_x):
            max_x = pos.x
        if (pos.y > max_y):
            max_y = pos.y

    render = scene.render
    
    p_min_x = int(min_x * render.resolution_x)
    p_min_y = int(min_y * render.resolution_y)
    p_max_x = int(max_x * render.resolution_x)
    p_max_y = int(max_y * render.resolution_y)
    
    return [p_min_x, p_min_y, p_max_x, p_max_y]


ANNOTATIONS = {}


def save_image(i, name, camera, scene, object):
    name = 'img_' + str(i) + '_' + name
    bpy.context.scene.render.filepath = 'D:/PROJECTS/homeworks/deepschool_3d_cv/08_hw/data/' + name + '.png'
    bpy.ops.render.render(write_still=True)
    ANNOTATIONS[name] = save_bbox(camera, scene, object)


def save_image_with_single_object(
        i, name, 
        object_name_01, object_name_02, name_object, 
        camera, scene, object
    ):
    
    bpy.data.objects[object_name_01].hide_render = False
    
    save_image(
        i, name + '_' + name_object + '_01', 
        camera, scene, object
    )
    
    bpy.data.objects[object_name_01].hide_render = True
    bpy.data.objects[object_name_02].hide_render = False
    
    save_image(
        i, name + '_' + name_object + '_02', 
        camera, scene, object
    )
    
    bpy.data.objects[object_name_02].hide_render = True


def save_image_with_multiple_object(
        i,name,
        object_name_01_01, object_name_01_02, 
        object_name_02_01, object_name_02_02, 
        object_name_03, 
        name_01, name_02,name_03,
        camera, scene, object
    ):
    
    bpy.data.objects[object_name_01_01].hide_render = False
    bpy.data.objects[object_name_02_01].hide_render = False
    
    save_image(
        i, name + '_' + name_01 + '_01_' + name_02 + '_01', 
        camera, scene, object
    )
    
    bpy.data.collections[object_name_03].hide_render = False
    
    save_image(
        i, name + '_' + name_01 + '_01_' + name_02 + '_01' + '_' + name_03, 
        camera, scene, object
    )
    
    bpy.data.collections[object_name_03].hide_render = True
    
    bpy.data.objects[object_name_02_01].hide_render = True
    bpy.data.objects[object_name_02_02].hide_render = False
    
    save_image(
        i, name + '_' + name_01 + '_01_' + name_02 + '_02', 
        camera, scene, object
    )
    
    bpy.data.collections[object_name_03].hide_render = False
    
    save_image(
        i, name + '_' + name_01 + '_01_' + name_02 + '_02' + '_' + name_03, 
        camera, scene, object
    )
    
    bpy.data.collections[object_name_03].hide_render = True
    
    bpy.data.objects[object_name_01_01].hide_render = True
    bpy.data.objects[object_name_01_02].hide_render = False
    bpy.data.objects[object_name_02_01].hide_render = False
    bpy.data.objects[object_name_02_02].hide_render = True
    
    save_image(
        i, name + '_' + name_01 + '_02_' + name_02 + '_01', 
        camera, scene, object
    )
    
    bpy.data.collections[object_name_03].hide_render = False
    
    save_image(
        i, name + '_' + name_01 + '_02_' + name_02 + '_01' + '_' + name_03, 
        camera, scene, object
    )
    
    bpy.data.collections[object_name_03].hide_render = True
    
    bpy.data.objects[object_name_02_01].hide_render = True
    bpy.data.objects[object_name_02_02].hide_render = False
    
    save_image(
        i, name + '_' + name_01 + '_02_' + name_02 + '_02', 
        camera, scene, object
    )
    
    bpy.data.collections[object_name_03].hide_render = False
    
    save_image(
        i, name + '_' + name_01 + '_02_' + name_02 + '_02' + '_' + name_03, 
        camera, scene, object
    )
    
    bpy.data.collections[object_name_03].hide_render = True
    
    bpy.data.objects[object_name_01_02].hide_render = True
    bpy.data.objects[object_name_02_02].hide_render = True


def save_images(
        i,name, 
        object_name_01_01, object_name_01_02, 
        object_name_02_01, object_name_02_02, 
        object_name_03,
        name_01, name_02, name_03,
        camera, scene, object
    ):
    
    # STREET
    save_image(i, name, camera, scene, object)
    
    # STREET + MAN
    save_image_with_single_object(
        i, name, 
        object_name_01_01, object_name_01_02, name_01, 
        camera, scene, object
    )
    
    # STREET + WOMAN
    save_image_with_single_object(
        i, name, 
        object_name_02_01, object_name_02_02, name_02, 
        camera, scene, object
    )
    
    # STREET + MAN + WOMAN
    save_image_with_multiple_object(
        i, name, 
        object_name_01_01, object_name_01_02, 
        object_name_02_01, object_name_02_02, 
        object_name_03, 
        name_01, name_02, name_03,
        camera, scene, object
    )        


cam = bpy.data.objects['Camera']
scene = bpy.context.scene
object = bpy.context.object
#object = bpy.data.objects['stop sign']


cam.rotation_euler = (math.pi / 2, 0, 0)

target_angle = 360
num_steps = 10
r = 10
t_loc_x = 0
t_loc_y = 0


for i in range(num_steps):
    alpha = i * target_angle / num_steps

    cam.rotation_euler[2] = math.pi / 2 + alpha

    cam.location.x = t_loc_x + math.cos(alpha) * r
    cam.location.y = t_loc_y + math.sin(alpha) * r

    #bpy.context.scene.render.film_transparent = True
    #bpy.context.scene.render.image_settings.color_mode = 'RGBA'
    
    bpy.data.objects['street_01'].hide_render = False
    
    save_images(
        i, 'street_01',
        'athletic_african_walking_01', 'athletic_african_walking_02',
        'mei_posed_01', 'mei_posed_02',
        'police_car_01',
        'man', 'woman', 'car',
        cam, scene, object
    )
    
    bpy.data.objects['street_01'].hide_render = True
    bpy.data.objects['street_02'].hide_render = False
    
    save_images(
        i, 'street_02',
        'athletic_african_walking_03', 'athletic_african_walking_04',
        'mei_posed_03', 'mei_posed_04',
        'police_car_02',
        'man', 'woman', 'car',
        cam, scene, object
    )
    
    bpy.data.objects['street_02'].hide_render = True
    bpy.data.objects['street_03'].hide_render = False
    
    save_images(
        i, 'street_03',
        'athletic_african_walking_05', 'athletic_african_walking_06',
        'mei_posed_05', 'mei_posed_06',
        'police_car_03',
        'man', 'woman', 'car',
        cam, scene, object
    )
    
    bpy.data.objects['street_03'].hide_render = True
    bpy.data.objects['street_04'].hide_render = False
    
    save_images(
        i, 'street_04',
        'athletic_african_walking_07', 'athletic_african_walking_08',
        'mei_posed_07', 'mei_posed_08',
        'police_car_04',
        'man', 'woman', 'car',
        cam, scene, object
    )
    
    bpy.data.objects['street_04'].hide_render = True
    bpy.data.objects['street_05'].hide_render = False
    
    save_images(
        i, 'street_05',
        'athletic_african_walking_09', 'athletic_african_walking_10',
        'mei_posed_09', 'mei_posed_10',
        'police_car_05',
        'man', 'woman', 'car',
        cam, scene, object
    )

    #bpy.context.scene.render.film_transparent = False
    #bpy.context.scene.render.image_settings.color_mode = 'RGB'

    #bpy.data.objects[''].hide_render = True
    
    # INIT
    
    bpy.data.objects['street_05'].hide_render = True


with open('D:/PROJECTS/homeworks/deepschool_3d_cv/08_hw/annotations.csv', 'w') as file:
    for key, value in ANNOTATIONS.items():
        file.write(str(key) + ';' + str(value) + '\n')