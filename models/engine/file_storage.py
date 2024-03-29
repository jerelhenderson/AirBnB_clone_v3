#!/usr/bin/python3
'''
    Define class FileStorage
'''
import json
import models


class FileStorage:
    '''
        Serializes instances to JSON file and deserializes to JSON file.
    '''
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        '''
            Return the dictionary
        '''
        if cls is None:
            return self.__objects
        else:
            my_dict = {}
            for k, v in self.__objects.items():
                name = k.split('.')
                if name[0] in str(cls):
                    my_dict[k] = v
            return my_dict

    def get(self, cls, id):
        """Returns obj based on class name and ID; return None if not found"""
        cls_dict = self.all(cls)
        key = cls + '.' + id
        return cls_dict[key] if key in cls_dict else None

    def count(self, cls=None):
        """Returns num of objs in storage matching the given class name;
        return count of all objs if no name is passed
        """
        return len(self.all()) if not cls else len(self.all(cls))

    def new(self, obj):
        '''
            Set in __objects the obj with key <obj class name>.id
            Aguments:
                obj : An instance object.
        '''
        key = str(obj.__class__.__name__) + "." + str(obj.id)
        value_dict = obj
        FileStorage.__objects[key] = value_dict

    def save(self):
        '''
            Serializes __objects attribute to JSON file.
        '''
        objects_dict = {}
        for key, val in FileStorage.__objects.items():
            objects_dict[key] = val.to_dict()

        with open(FileStorage.__file_path, mode='w', encoding="UTF8") as fd:
            json.dump(objects_dict, fd)

    def reload(self):
        '''
            Deserializes the JSON file to __objects.
        '''
        try:
            with open(FileStorage.__file_path, encoding="UTF8") as fd:
                FileStorage.__objects = json.load(fd)
            for key, val in FileStorage.__objects.items():
                class_name = val["__class__"]
                class_name = models.classes[class_name]
                FileStorage.__objects[key] = class_name(**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        '''
        Deletes an object from __objects if it is inside of __objects
        '''
        copy_storage = dict(FileStorage.__objects)
        desired_key = obj
        for key, val in copy_storage.items():
            if val == desired_key:
                del(obj)
                del FileStorage.__objects[key]
                self.save()

    def close(self):
        '''
        Method calls reload method to deserialize JSON file to objects
        '''
        self.reload()
