'''
Created on 12-Dec-2016

@author: root
'''
'''
import packages
'''
import random
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
            maxLength = 10
        else:
            minLength = m["maxLength"]     
        return(minLength,maxLength)

    '''
    Generate a random word of given length
    '''
    def randomword(self, length, pattern):
        random_str = exrex.getone(pattern)[:1]
        for i in range(length - 1):
            random_str = random_str + (exrex.getone(pattern)[:1])
        return random_str

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
    def get_param_value(self, value_type, param_type, param_name, scenerio, m, enum_value = []):
        if(scenerio == 'positive'):
            if (value_type == "lower_boundary"):
                
                            if (len(enum_value) > 0):
                                self.parameter_value = random.choice(enum_value)
                                                
                            elif (param_type == "integer"):
                                minimum, maximum = self.get_min_max_values(m)
                                self.parameter_value = minimum
                                
                                
                            elif (param_type == "string"):
                                minLength, maxLength = self.get_min_max_length(m)
                                if 'pattern' not in m:
                                    pattern = "^[a-zA-Z0-9]*$"
                                else:
                                    pattern = m["pattern"]
                                self.parameter_value = self.randomword(minLength, pattern)
                                
                                
                            elif ('client.get_model' in param_type):
                                self.parameter_value = param_type                                     
                                
                            else:
                                self.parameter_value = "UnsupportedDatatype"                
                
            elif (value_type == "upper_boundary"):
                
                            if (len(enum_value) > 0):
                                self.parameter_value = random.choice(enum_value)                
                
                            elif (param_type == "integer"):
                                minimum, maximum = self.get_min_max_values(m)
                                self.parameter_value = maximum

                            elif (param_type == "string"):
                                minLength, maxLength = self.get_min_max_length(m)
                                if 'pattern' not in m:
                                    pattern = "^[a-zA-Z0-9]*$"
                                else:
                                    pattern = m["pattern"]
                                self.parameter_value = self.randomword(maxLength, pattern)
                                
                                
                            elif ('client.get_model' in param_type):
                                self.parameter_value = param_type                                     
                                
                            else:
                                self.parameter_value = "UnsupportedDatatype"                
                
                
                
            elif (value_type == "random"):
                
                            if (len(enum_value) > 0):
                                self.parameter_value = random.choice(enum_value)                
                
                            elif (param_type == "integer"):
                                minimum, maximum = self.get_min_max_values(m)
                                self.parameter_value = randint(minimum + 1, maximum - 1)
                                
                            elif (param_type == "string"):
                                minLength, maxLength = self.get_min_max_length(m)
                                if 'pattern' not in m:
                                    pattern = "^[a-zA-Z0-9]*$"
                                else:
                                    pattern = m["pattern"]
                                self.parameter_value = self.randomword(randint(minLength + 1, maxLength - 1), pattern)
                                
                            elif ('client.get_model' in param_type):
                                self.parameter_value = param_type                                     
                                
                            else:
                                self.parameter_value = "UnsupportedDatatype"                         
            
                
        elif(scenerio == 'negative'):
            if (value_type == "lower_boundary"):
                
                            if (param_type == "integer"):
                                minimum, maximum = self.get_min_max_values(m)
                                self.parameter_value = minimum - 1
                                
                            elif (param_type == "string"):
                                minLength, maxLength = self.get_min_max_length(m)
                                pattern = "^[%@~!*+]*$"                                
                                self.parameter_value = self.randomword(minLength, pattern)
                                
                                
                            elif ('client.get_model' in param_type):
                                self.parameter_value = param_type                                     
                                
                            else:
                                self.parameter_value = "UnsupportedDatatype"                
                
            elif (value_type == "upper_boundary"):
                
                            if (param_type == "integer"):
                                minimum, maximum = self.get_min_max_values(m)
                                self.parameter_value = maximum + 1
                                
                            elif (param_type == "string"):
                                minLength, maxLength = self.get_min_max_length(m)
                                pattern = "^[%@~!*+]*$"                                
                                self.parameter_value = self.randomword(maxLength + 1, pattern)
                                
                                
                            elif ('client.get_model' in param_type):
                                self.parameter_value = param_type                                     
                                
                            else:
                                self.parameter_value = "UnsupportedDatatype"                
                
                
                
            elif (value_type == "random"):
                
                            if (param_type == "integer"):
                                minimum, maximum = self.get_min_max_values(m)
                                self.parameter_value = minimum - randint(minimum + 1, maximum)
                                
                            elif (param_type == "string"):
                                minLength, maxLength = self.get_min_max_length(m)
                                pattern = "^[%@~!*+]*$"
                                self.parameter_value = self.randomword(randint(minLength , maxLength), pattern)
                                
                            elif ('client.get_model' in param_type):
                                self.parameter_value = param_type                                     
                                
                            else:
                                self.parameter_value = "UnsupportedDatatype"                         
            
        return self.parameter_value