#!/usr/bin/env python3
# -*- coding: utf-8 -*
# sample_python aims to allow seamless integration with lua.
# see examples below

import os
import sys
import pdb  # use pdb.set_trace() for debugging
import code # or use code.interact(local=dict(globals(), **locals()))  for debugging.
import xml.etree.ElementTree as ET
import numpy as np
from PIL import Image

class Color:
    def __init__(self, R, G, B):
        self.color=np.array([R,G,B]).astype(np.float64)

    # Gamma corrects this color.
    # @param gamma the gamma value to use (2.2 is generally used).
    def gammaCorrect(self, gamma):
        inverseGamma = 1.0 / gamma
        self.color=np.power(self.color, inverseGamma)

    def toUINT8(self):
        return (np.clip(self.color, 0,1)*255).astype(np.uint8)
    
class Shader:
    def __init__(self, type, diffuseColor, specularColor, exponent):
        self.type = type # type is lambertian or phong
        self.diffuseColor = diffuseColor
        self.specularColor = specularColor
        self.exponent = exponent

class Sphere:
    def __init__(self, center, radius, shader):
        self.center = center
        self.radius = radius
        self.shader = shader

class Light:
    def __init__(self, position, intensity):
        self.position = position
        self.intensity = intensity

def trace_intersection(viewPoint, ray, sphere_list):
    closest_intersection_index = -1 # -1 is no intersection
    closest_intersection_distance = float('inf') # infinity is no intersection

    for i, sphere in enumerate(sphere_list):
        a = np.dot(ray, ray)
        b = np.dot((viewPoint - sphere.center), ray)
        c = np.dot((viewPoint - sphere.center), (viewPoint - sphere.center)) - sphere.radius**2
        D = b**2 - a*c

        if D >= 0:
            t0 = (-b - np.sqrt(D)) / a
            t1 = (-b + np.sqrt(D)) / a

            if t1 >= 0 and t1 <= closest_intersection_distance:
                closest_intersection_distance = t1
                closest_intersection_index = i
            if t0 >= 0 and t0 <= closest_intersection_distance:
                closest_intersection_distance = t0
                closest_intersection_index = i

    return [closest_intersection_distance, closest_intersection_index]

def shade(intersection, ray, viewPoint, sphere_list, light):    
    surface = sphere_list[intersection[1]]
    r,g,b = 0, 0, 0
    
    intersection_point = viewPoint + intersection[0]*ray
    
    p = intersection_point - surface.center
    unit_p = p / np.linalg.norm(p)
    
    view_vec = viewPoint - intersection_point
    unit_view_vec = view_vec / np.linalg.norm(view_vec)

    light_vec = view_vec + light.position - viewPoint
    unit_light_vec = light_vec / np.linalg.norm(light_vec)
    
    light_intersection = trace_intersection(light.position, -unit_light_vec, sphere_list)
    if light_intersection[1] == intersection[1]:
        r += surface.shader.diffuseColor[0] * light.intensity[0] * max(0, np.dot(unit_p, unit_light_vec))
        g += surface.shader.diffuseColor[1] * light.intensity[1] * max(0, np.dot(unit_p, unit_light_vec))
        b += surface.shader.diffuseColor[2] * light.intensity[2] * max(0, np.dot(unit_p, unit_light_vec))

        if surface.shader.specularColor is not None and surface.shader.exponent is not None:
            half_vector = (unit_view_vec + unit_light_vec) / np.linalg.norm(unit_view_vec + unit_light_vec)
            r += surface.shader.specularColor[0] * light.intensity[0] * (max(0, np.dot(p, half_vector))**surface.shader.exponent)
            g += surface.shader.specularColor[1] * light.intensity[1] * (max(0, np.dot(p, half_vector))**surface.shader.exponent)
            b += surface.shader.specularColor[2] * light.intensity[2] * (max(0, np.dot(p, half_vector))**surface.shader.exponent)
        
    color = Color(r, g, b)
    color.gammaCorrect(2.2)
    return color.toUINT8()

def main():
    tree = ET.parse(sys.argv[1])
    root = tree.getroot()

    # set default values
    viewDir=np.array([0,0,-1]).astype(np.float64)
    viewUp=np.array([0,1,0]).astype(np.float64)
    viewProjNormal=-1*viewDir  # you can safely assume this. (no examples will use shifted perspective camera)
    viewWidth=1.0
    viewHeight=1.0
    projDistance=1.0
    intensity=np.array([1,1,1]).astype(np.float64)  # how bright the light is.
    print(np.cross(viewDir, viewUp))

    imgSize=np.array(root.findtext('image').split()).astype(np.int32)

    for c in root.findall('camera'):
        viewPoint=np.array(c.findtext('viewPoint').split()).astype(np.float64)
        print('viewpoint', viewPoint)
        viewDir = np.array(c.findtext('viewDir').split()).astype(np.float64)
        viewUp = np.array(c.findtext('viewUp').split()).astype(np.float64)
        viewProjNormal = np.array(c.findtext('projNormal').split()).astype(np.float64)
        viewWidth = np.array(c.findtext('viewWidth')).astype(np.float64)
        viewHeight = np.array(c.findtext('viewHeight')).astype(np.float64)
        if(c.findtext('projDistance') is not None):
            projDistance = np.array(c.findtext('projDistance')).astype(np.float64)
        
    sphere_list = []
    for s in root.findall('surface'):
        center = np.array(s.findtext('center').split()).astype(np.float64)
        radius = np.array(s.findtext('radius')).astype(np.float64)
        ref = s.find('shader').get('ref') # find는 태그 이름 찾기 get은 태그 속성값 찾기 findtext 태그 내부 값 찾기
        
        for sh in root.findall('shader'):
            name = sh.get('name')
            sh_type = sh.get('type')
            if name == ref:
                diffuseColor = np.array(sh.findtext('diffuseColor').split()).astype(np.float64)
                if(sh.findtext('specularColor') is not None and sh.findtext('exponent') is not None): # Phong
                    specularColor = np.array(sh.findtext('specularColor').split()).astype(np.float64)
                    exponent = np.array(sh.findtext('exponent')).astype(np.float64)
                else : # Lambertian
                    specularColor, exponent = None, None
                shader = Shader(sh_type, diffuseColor, specularColor, exponent)
                sphere_list.append(Sphere(center, radius, shader))
                break
    
    for l in root.findall('light'):
        position = np.array(l.findtext('position').split()).astype(np.float64)
        intensity = np.array(l.findtext('intensity').split()).astype(np.float64)
        light = Light(position, intensity)
        
    #code.interact(local=dict(globals(), **locals()))  

    # Create an empty image
    channels=3
    img = np.zeros((imgSize[1], imgSize[0], channels), dtype=np.uint8)
    img[:,:]=0
    
    # replace the code block below!

    w = viewDir
    u = np.cross(w, viewUp)
    v = np.cross(w, u)

    unit_w = w / np.linalg.norm(w)
    unit_u = u / np.linalg.norm(u)
    unit_v = v / np.linalg.norm(v)

    origin_lb = unit_w*projDistance - unit_u*viewWidth/2 - unit_v*viewHeight/2 + viewPoint
    
    for x in np.arange(imgSize[0]):
        for y in np.arange(imgSize[1]):
            # u = l + (r - l) * (i + 0.5) / nx
            # v = b + (t - b) * (j + 0.5) / ny
            ray = origin_lb + unit_u*viewWidth*(x+0.5)/imgSize[0] + unit_v*viewHeight*(y+0.5)/imgSize[1] - viewPoint
            intersection = trace_intersection(viewPoint, ray, sphere_list)
            if(intersection[1] != -1):
                img[y][x] = shade(intersection, ray, viewPoint, sphere_list, light)

    rawimg = Image.fromarray(img, 'RGB')
    #rawimg.save('out.png')
    rawimg.save(sys.argv[1]+'.png')
    
if __name__=="__main__":
    main()