# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 10:33:05 2019

@author: Xiepeng
"""
#CM:0
#P:1
#CSP:2
#CH:3
#T:4
inf_kind={"CM":1,"P":2,"CSP":3,"CH":4,"T":5}
path_cere='C:\\Users\\LKJ\\Desktop\\new_part_five\\cerebellum\\train\\xml'
image_id=1
ci=1
import os
import json
from xml.dom.minidom import parse
xml_files=os.listdir(path_cere)
information_all_pic={}
id_annotations=1
for single_xml in xml_files:
    path_xmll=path_cere+'\\'+single_xml
    xml_ = parse(path_xmll)
    txt_=xml_.documentElement
    #print(txt_.toxml())
    filename=xml_.getElementsByTagName('filename')
    #print('filename_counts:',len(filename))
    img_name=filename[0].toxml()[10:-11]
    #print(img_name)
    img_width=xml_.getElementsByTagName('width')[0].toxml()[7:-8]
    img_height=xml_.getElementsByTagName('height')[0].toxml()[8:-9]
    kinds=xml_.getElementsByTagName('object')
    #print('number_of_kind:',len(kinds))
    annotations={}
    for kind in kinds:
        #print(len(kind.childNodes))
        #print('kind:',kind.childNodes[1].toxml()[6:-7])
        kind_=kind.childNodes[1].toxml()[6:-7]
        if kind_ == "csp":
           kind_ = "CSP"
        if kind_ == "cerebellum":
           kind_ = "CH"
        category_id=inf_kind[kind_]
        #print(kind.childNodes[9].childNodes[1].toxml()[6:-7])#xmin
        x=kind.childNodes[9].childNodes[1].toxml()[6:-7]
        #print(kind.childNodes[9].childNodes[3].toxml()[6:-7])#ymin
        y=kind.childNodes[9].childNodes[3].toxml()[6:-7]
        #print(kind.childNodes[9].childNodes[5].toxml()[6:-7])#xmax
        width=str(int(kind.childNodes[9].childNodes[5].toxml()[6:-7])-int(x))
        #print(kind.childNodes[9].childNodes[7].toxml()[6:-7])#ymax
        height=str(int(kind.childNodes[9].childNodes[7].toxml()[6:-7])-int(y))
        annotations[(x,y,width,height)]=category_id
        information_all_pic[ci]={'img_width':img_width,'img_height':img_height,'annotations':annotations}
        information_all_pic[ci]['id_bbox']=id_annotations
        id_annotations +=1
    information_all_pic[ci]['file_name']=single_xml[:-4]+'.jpg'
    information_all_pic[ci]['id']=image_id
    image_id+=1
    ci+=1
#print(information_all_pic)
all_={}
images={}
infor_list=[]
annotations_list=[]
annot_dic_if={}
print('counts of pic:',len(information_all_pic))
for single_id in information_all_pic:
    #print(single_id)
    single_dic={}
    single_dic["file_name"]=information_all_pic[single_id]['file_name']
    single_dic["height"]=information_all_pic[single_id]['img_height']
    single_dic["width"]=information_all_pic[single_id]['img_width']
    single_dic["id"]=information_all_pic[single_id]['id']
    infor_list.append(single_dic)
#{"segmentation":[[56,0,56,150,164,150,164,0]],
# "area":16200,
# "iscrowd":0,
# "image_id":2008000015,
# "bbox":[56,0,108,150],
# "category_id":5,
# "id":4,
# "ignore":0}
    segmentation=[[56,0,56,150,164,150,164,0]]
    area=16200
    iscrowd=0
    #category_id=2
    #print(information_all_pic[single_id]['annotations'])
    for box in information_all_pic[single_id]['annotations']:
        annot_dic_if["segmentation"]=segmentation
        annot_dic_if["area"]=area
        annot_dic_if["iscrow"]=iscrowd
        annot_dic_if["bbox"]=box
        annot_dic_if["category_id"]=information_all_pic[single_id]['annotations'][box]
        annot_dic_if["image_id"]=single_dic["id"]
        annot_dic_if["id"]=information_all_pic[single_id]['id_bbox']
        #print(annot_dic_if)
        annotations_list.append(annot_dic_if)
#[
#{"supercategory":"none","id":1,"name":"aeroplane"},
#{"supercategory":"none","id":2,"name":"bicycle"},
#{"supercategory":"none","id":3,"name":"bird"},
#{"supercategory":"none","id":4,"name":"boat"},
#{"supercategory":"none","id":5,"name":"bottle"}
#]
catg_list=[]
for sin_ in inf_kind:
    dic_catg={}
    dic_catg["name"]=sin_
    dic_catg["id"]=inf_kind[sin_]
    dic_catg["supercategory"]="none"
    catg_list.append(dic_catg)
#print(catg_list)
all_["images"]=infor_list
all_["annotations"]=annotations_list
all_["categories"]=catg_list
with open ('C:\\Users\\LKJ\\Desktop\\new_part_five\\cerebellum\\train\\cere_train2019.json','w') as json_t:
    json_t.write(json.dumps(all_))























