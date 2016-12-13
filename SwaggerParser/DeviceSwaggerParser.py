'''
Created on 12-Dec-2016

@author: root
'''
'''
import packages and Constants
'''
import yaml
from Config import Constants
from Config.Constants import positive_testfunc_file, negative_testfunc_file, networkdevices_swagger
import DeviceSwaggerParserHelper

class DeviceSwaggerParser(DeviceSwaggerParserHelper.DeviceSwaggerParserHelper):

    def __init__(self):
        '''
        Declare lists
        '''
        self.parameter_name, self.parameter_type, self.parameter_data, self.parameter_value, self.parameter_func = ([] for i in range(5))
        '''
        Empty the files containing TestCase Functions
        ''' 
        open(positive_testfunc_file, 'w').close()
        open(negative_testfunc_file, 'w').close()
    
    '''
    Evaluate inner parameters of function
    '''    
    def get_param_func(self, m, scenerio):
        if 'name' in m and 'type' in m:
            param_type = m["type"]
            param_name = m["name"]
        elif '$ref' in m:
            if 'parameter' in m["$ref"]:
                ref = m["$ref"].replace('#/parameters/', '')
                param_type = self.get_datatype(ref)
                param_name = ref
        
        self.parameter_value = self.get_param_value(param_type, param_name, scenerio , m)
        self.parameter_func.append(param_name+"="+str(self.parameter_value))       
        return self.parameter_func

    '''
    Evaluate Nested Objects within Swagger
    '''
    def get_innerobjtype_func(self, ref, scenerio, m):
        param_func = []
        params = self.get_definition_datatype(ref, scenerio)
        for keys,values in params.items():
            self.parameter_value = self.get_param_value(values, keys, scenerio , m)
            param_func.append(keys+"--"+str(self.parameter_value))
            
        brav_func = "client.get_model{"+ref+"}{"+",".join(param_func).replace(',',':')+"}"
        return brav_func    
    
    '''
    Evaluate Object Type parameters from Swagger
    '''
    def get_objtype_func(self, m,scenerio):
        param_func = []
        ref = m["schema"]["$ref"].replace('#/definitions/','')
        params = self.get_definition_datatype(ref, scenerio)
    
        for keys,values in params.items():
            self.parameter_value = self.get_param_value(values, keys, scenerio , m)
            param_func.append(keys+":-"+str(self.parameter_value))
            
        brav_func = ref+"=client.get_model["+ref+"]["+",".join(param_func).replace(',',';')+"])"
        return brav_func

    '''
    Get DataType of parameters from Swagger file
    '''
    def get_datatype(self, ref):
        with open(networkdevices_swagger, 'r') as f:    
            doc = yaml.load(f)
    
        data = doc["parameters"]
        for k in data.keys():
            if (k in [ref]):
                ref_datatype = data[k]['type']
                return ref_datatype
        
        
    '''
    Get DataType of parameters defined inside definitions
    '''    
    def get_definition_datatype(self, ref, scenerio):
        param_type = []
        params = {}
        with open(networkdevices_swagger, 'r') as f:    
            doc = yaml.load(f)
    
        data = doc["definitions"]
        for k in data.keys():
            if k == ref:
                for l in data[k].keys():
                    if l == 'properties':
                        for m in data[k][l].keys():
                            for n in data[k][l][m].keys():
                                if 'type' in n:
                                    param_type.append(data[k][l][m]["type"])
                                    params[m] = data[k][l][m]["type"]
                                
                                if '$ref' in n:
                                    ref = data[k][l][m]["$ref"].replace('#/definitions/','')
                                    params[m] = obj.get_innerobjtype_func(ref, scenerio, m)
        return params
        
        

'''
Parse the Network Swagger yaml file to find the function names along with parameters for positive and negative scenerios and store in the files 
'''
obj = DeviceSwaggerParser()
with open(networkdevices_swagger, 'r') as f:  
    doc = yaml.load(f)
data = doc["paths"]
for scenerio in Constants.scenerio_list:
    for k in data.keys():
        for l in data[k].keys():
            func_name =  data[k][l]["operationId"]
            tag_name = data[k][l]["tags"][0]
            obj_flag = 0
            try:
                    for m in data[k][l]["parameters"]:
                        
                        if 'in' in m:
                            if(m['in'] == "body"):
                                objtype_func = obj.get_objtype_func(m, scenerio)
                                obj_flag = 1
                            else:
                                obj.parameter_func = obj.get_param_func(m,scenerio)
                                
                        else:
                            obj.parameter_func = obj.get_param_func(m,scenerio)
                    
                    if(obj_flag == 1):
                        bravado_func = func_name+"("+",".join(obj.parameter_func)+","+"".join(objtype_func)
                        print(bravado_func, tag_name)
                    else:
                        bravado_func = func_name+"("+",".join(obj.parameter_func)+")"
                        print(bravado_func, tag_name)
                    
                    if (scenerio == 'positive'):
                        obj.save_bravado_func(bravado_func, tag_name, positive_testfunc_file)
                    elif (scenerio == 'negative'):
                        obj.save_bravado_func(bravado_func, tag_name, negative_testfunc_file)
            
            except Exception as e:
                    print str(e)
                
            obj.parameter_name, obj.parameter_type, obj.parameter_data, obj.parameter_value, obj.parameter_func = ([] for i in range(5))                
