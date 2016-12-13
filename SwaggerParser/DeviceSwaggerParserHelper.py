'''
Created on 12-Dec-2016

@author: root
'''
'''
import packages
'''
import random, string
import exrex
from random import randint
from Config import Constants

class DeviceSwaggerParserHelper(object):
    '''
    Get minimum and maximum value of Integer type parameters from Swagger file
    ''' 
    def get_min_max_values(self,m):
        if 'minimum' not in m:
            minimum = 1
        else:
            minimum = m["minimum"]
        if 'maximum' not in m:
            maximum = 10
        else:
            maximum = m["maximum"]     
        return(minimum,maximum)
    
    '''
    Get minimum and maximum length of String type parameters from Swagger file
    ''' 
    def get_min_max_length(self, m):
        if 'minLength' not in m:
            minLength = 1
        else:
            maxLength = m["maxLength"]
        if 'maxLength' not in m:
            maxLength = 100
        else:
            minLength = m["maxLength"]     
        return(minLength,maxLength)

    '''
    Generate a random word of given length
    '''
    def randomword(self, length):
        return ''.join(random.choice(string.lowercase) for i in range(length))

    '''
    Generate a random word for the given pattern
    '''
    def generate_pattern_matching_string(self, pattern):
        return(exrex.getone(pattern))

    '''
    Redirect positive and negative scenerio's function names to their respective files
    '''
    def save_bravado_func(self, bravado_func, tag_name, filename):
        f1=open(filename,"a")
        print >>f1, bravado_func, '&&' , tag_name
        
        
    '''
    Get Parameter Values
    '''
    def get_param_value(self, param_type, param_name, scenerio, m):
        if(scenerio == 'positive'):
                            if (param_type == "integer"):
                                minimum, maximum = self.get_min_max_values(m)
                                self.parameter_value = randint(minimum, maximum)
                                
                            elif (param_type == "string" and param_name =='device_type'):
                                self.parameter_value = random.choice(Constants.devices_type) 
                            
                            elif (param_type == "string"):
                                self.parameter_value = random.choice(Constants.devices) 
                                
                            elif ('client.get_model' in param_type):
                                self.parameter_value = param_type                                     
                                
                            else:
                                self.parameter_value = "Vijay"
                                  
        elif(scenerio == 'negative'):
                            if (param_type == "integer"):
                                minimum, maximum = self.get_min_max_values(m)
                                self.parameter_value = minimum - 1
  
                            elif (param_type == "string"):
                                self.parameter_value = random.choice(Constants.invalid_devices)
                                
                            elif ('client.get_model' in param_type):
                                self.parameter_value = param_type                                  
                                
                            else:
                                self.parameter_value = "Vijay" 
                                
        return self.parameter_value