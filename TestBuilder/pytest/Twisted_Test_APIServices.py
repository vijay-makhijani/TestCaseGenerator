#! /usr/bin/env py.test
import sys
    
'''
Test Positive Test Case Scenerios using Pytest and Twisted
'''

def test_positivecase_device_operations(testdir):
    testdir.makepyfile("""

import os
import re
import pytest
import yaml
from twisted.internet import reactor, defer
from twisted.internet.defer import Deferred, DeferredList
from bravado.client import SwaggerClient
from bravado_core.exception import SwaggerMappingError

global func_dict
project_path = "/opt/AutomationWorkSpace/GenericTestCaseGenerator"
positive_testcase_log_file = project_path+"/TestBuilder/output_files/positive_testcase_log_file"
positive_testfunc_file = project_path+"/SwaggerParser/output_files/positive_testfunc_file"
networkdevices_swagger = project_path+"/SwaggerConnexion/networkdevices_swagger.yaml"
open(positive_testcase_log_file, 'w').close()  
client = SwaggerClient.from_url("http://localhost:8080/swagger.json", config={'also_return_response': True, 'validate_responses': False, 'validate_requests': False, 'validate_swagger_spec': False})

@pytest.fixture
def networkDevice():
    return SwaggerClient.from_url('http://localhost:8080/swagger.json', config={'also_return_response': True, 'validate_responses': False, 'validate_requests': False, 'validate_swagger_spec': False})

def get_innerobj_paramvalue(argvalue):
    obj_model = "{".join(argvalue.split("{", 2)[:2])
    obj_model_name = obj_model[obj_model.find("{")+1:obj_model.find("}")]
    methodToCall = getattr(client, 'get_model')
    result = methodToCall(obj_model_name)
    
    objindex = argvalue.split("}")
    objindex[1] = objindex[1].replace('{', '')
        
    innerparamindex = objindex[1].split(':')
    paramdict = dict()
    for item in innerparamindex:
        # Separate the parameter name and value
        paramname, paramvalue = item.split('--')
        # Add it to the dictionary
        if 'get_model' in paramvalue:
            paramvalue = get_innerobj_paramvalue(paramvalue)
        
        int_type_parameters = get_integer_parameters()
        if (paramname in int_type_parameters):
            paramvalue = int(paramvalue)
        paramdict.update({paramname: paramvalue})
        # Call our function
    dict_obj = result(**paramdict)   
    return dict_obj



def get_obj_argvalue(argvalue):
    obj_model = "[".join(argvalue.split("[", 2)[:2])
    obj_model_name = obj_model[obj_model.find("[")+1:obj_model.find("]")]
    methodToCall = getattr(client, 'get_model')
    result = methodToCall(obj_model_name)
    
    objindex = argvalue.split("]")
    objindex[1] = objindex[1].replace('[', '')
        
    innerparamindex = objindex[1].split(';')
    paramdict = dict()
    for item in innerparamindex:
        # Separate the parameter name and value
        paramname, paramvalue = item.split(':-')
        # Add it to the dictionary
        if 'get_model' in paramvalue:
            paramvalue = get_innerobj_paramvalue(paramvalue)
        
        int_type_parameters = get_integer_parameters()
        if (paramname in int_type_parameters):
            paramvalue = int(paramvalue)
        paramdict.update({paramname: paramvalue})
        # Call our function
    dict_obj = result(**paramdict)   
    return dict_obj


def get_func_name(bravado_func):
    funcname, argsstr = bravado_func.split('(')
    # Split the parameters
    argsindex = argsstr.split(',')
    # Create an empty dictionary
    argsdict = dict()
    # Remove the closing parenthesis
    argsindex[-1] = argsindex[-1].replace(')', '')
    for item in argsindex:
        # Separate the parameter name and value
        argname, argvalue = item.split('=')
        if 'get_model' in argvalue:
            argvalue = get_obj_argvalue(argvalue)
        
        # Add it to the dictionary
        int_type_parameters = get_integer_parameters()
        if (argname in int_type_parameters):
            argvalue = int(argvalue)
        argsdict.update({argname: argvalue})
        # Call our function
    return (argsdict,funcname) 
    
   
def get_integer_parameters():
    int_type_parameters = []
    with open(networkdevices_swagger, 'r') as f:    
        doc = yaml.load(f)
        data = doc["paths"]
        for k in data.keys():
            for l in data[k].keys():
                    for m in data[k][l]["parameters"]:
                        if 'type' in m:
                            if (m["type"] == 'integer'):
                                int_type_parameters.append(m["name"])
        
        data = doc["definitions"]
        for k in data.keys():
                for l in data[k].keys(): 
                    if l == 'properties':
                        for m in data[k][l].keys():
                            for n in data[k][l][m].keys():
                                if 'type' in n:  
                                    if (data[k][l][m]["type"] == "integer"):
                                         int_type_parameters.append(m) 
                                         
        data = doc["parameters"]
        for k in data.keys():
            if 'type' in data[k]:
                if (data[k]['type'] == "integer"):
                    int_type_parameters.append(k)
                
        return int_type_parameters



def process_Result(result):
    print "Success", result  
    
    
def process_Error(Failure):
    print "Error Occurred" , Failure


def get_func_output(methodToCall, argsdict):
    global func_dict
    f1=open(positive_testcase_log_file,"a")
    d = defer.Deferred()
    func_name = func_dict[methodToCall]
    try:
                result, http_response = methodToCall(**argsdict).result()
        
                if (result is None):
                    result_type = type(result)                
                  
                elif(type(result) is list):
                    if not result:
                        result_type = '<type \\'NoneType\\'>'
                    else:
                        for data in result:
                            if isinstance(data, unicode):
                                result_type = type(data.encode('utf8'))
                            else:
                                result_type = type(data)
                           
                elif isinstance(result, unicode):
                    result_type = type(result.encode('utf8'))
                      
                else:
                    result_type = type(result)
                       
                matches=re.findall(r'\\'(.+?)\\'',str(result_type))          
        
                print >>f1, "FunctionName:", func_name.replace('\\n',''), '&&', "HttpResponse:", http_response.status_code, "&&", "ResultType:", matches[0], '&&', "Result:", result
                reactor.callLater(1, d.callback, (http_response.status_code))#@UndefinedVariable
        
    except Exception as e:
        print >>f1, "FunctionName:", func_name.replace('\\n',''), '&&', "HttpResponse:", e.status_code, "&&", "ResultType:", "NoneType", '&&', "Result:", str(e)
        reactor.callLater(1, d.callback, str(e))#@UndefinedVariable
    return d    
    
    

def test_positive_scenerios(networkDevice):
    with open(positive_testfunc_file) as input_file:
        count = 0
        global func_dict
        twisted_dict = dict()
        func_dict = dict()
        open(positive_testcase_log_file, 'w').close() 
        for data in input_file:
        
            func_name, tag_name = data.split('&&')
            func_name = func_name.split('$')[0]
            tag_name = tag_name.replace(' ','')
            f1=open(positive_testcase_log_file,"a")
            
            argsdict, funcname = get_func_name(func_name)
            
            client_obj = 'networkDevice.'+tag_name
            methodToCall = getattr(eval(client_obj), funcname)
            
            func_dict.update({methodToCall:func_name})
            twisted_dict.update({methodToCall: argsdict})
            
        try:
            dl = DeferredList(get_func_output(methodToCall, argsdict) for methodToCall,argsdict in twisted_dict.items())
            dl.addCallback(process_Result)
            dl.addErrback(process_Error)
        except Exception as e:
            print>>f1, "Exception Occurred", str(e)
            print "Exception Occurred", str(e)

""")
         
    rr = testdir.run(sys.executable, "-m", "pytest", "--twisted")
    outcomes = rr.parseoutcomes()
    assert outcomes.get("passed") == 1             

 
   
'''
Test Negative Test Case Scenerios using Pytest and Twisted
'''
   
def test_negativecase_device_operations(testdir):
    testdir.makepyfile("""
           
import os
import pytest
import yaml
from twisted.internet import reactor, defer
from bravado.client import SwaggerClient
from twisted.internet.defer import Deferred, DeferredList

project_path = "/opt/AutomationWorkSpace/GenericTestCaseGenerator"
negative_testcase_log_file = project_path+"/TestBuilder/output_files/negative_testcase_log_file"
networkdevices_swagger = project_path+"/SwaggerConnexion/networkdevices_swagger.yaml"
negative_testfunc_file = project_path+"/SwaggerParser/output_files/negative_testfunc_file"
open(negative_testcase_log_file, 'w').close()
client = SwaggerClient.from_url("http://localhost:8080/swagger.json", config={'also_return_response': True, 'validate_responses': False, 'validate_requests': False, 'validate_swagger_spec': False})
   
@pytest.fixture
def networkDevice():
    return SwaggerClient.from_url('http://localhost:8080/swagger.json', config={'also_return_response': True, 'validate_responses': False, 'validate_requests': False, 'validate_swagger_spec': False})
   
def get_innerobj_paramvalue(argvalue):
    obj_model = "{".join(argvalue.split("{", 2)[:2])
    obj_model_name = obj_model[obj_model.find("{")+1:obj_model.find("}")]
    methodToCall = getattr(client, 'get_model')
    result = methodToCall(obj_model_name)
    
    objindex = argvalue.split("}")
    objindex[1] = objindex[1].replace('{', '')
        
    innerparamindex = objindex[1].split(':')
    paramdict = dict()
    for item in innerparamindex:
        # Separate the parameter name and value
        paramname, paramvalue = item.split('--')
        # Add it to the dictionary
        if 'get_model' in paramvalue:
            paramvalue = get_innerobj_paramvalue(paramvalue)
        
        int_type_parameters = get_integer_parameters()
        if (paramname in int_type_parameters):
            paramvalue = int(paramvalue)
        paramdict.update({paramname: paramvalue})
        # Call our function
    dict_obj = result(**paramdict)   
    return dict_obj

      
def get_obj_argvalue(argvalue):
    obj_model = "[".join(argvalue.split("[", 2)[:2])
    obj_model_name = obj_model[obj_model.find("[")+1:obj_model.find("]")]
    methodToCall = getattr(client, 'get_model')
    result = methodToCall(obj_model_name)
       
    objindex = argvalue.split("]")
    objindex[1] = objindex[1].replace('[', '')
           
    innerparamindex = objindex[1].split(';')
    paramdict = dict()
    for item in innerparamindex:
        # Separate the parameter name and value
        paramname, paramvalue = item.split(':-')
        # Add it to the dictionary
        if 'get_model' in paramvalue:
            paramvalue = get_innerobj_paramvalue(paramvalue)        
        
        int_type_parameters = get_integer_parameters()
        if (paramname in int_type_parameters):
            paramvalue = int(paramvalue)
        paramdict.update({paramname: paramvalue})
        # Call our function
    dict_obj = result(**paramdict)     
    return dict_obj
   
   
def get_func_name(bravado_func):
    funcname, argsstr = bravado_func.split('(')
    # Split the parameters
    argsindex = argsstr.split(',')
    # Create an empty dictionary
    argsdict = dict()
    # Remove the closing parenthesis
    argsindex[-1] = argsindex[-1].replace(')', '')
    for item in argsindex:
        # Separate the parameter name and value
        argname, argvalue = item.split('=')
        if 'get_model' in argvalue:
            argvalue = get_obj_argvalue(argvalue)
           
        # Add it to the dictionary
        int_type_parameters = get_integer_parameters()
        if (argname in int_type_parameters):
            argvalue = int(argvalue)
        argsdict.update({argname: argvalue})
        # Call our function
    return (argsdict,funcname) 
       
      
def get_integer_parameters():
    int_type_parameters = []
    with open(networkdevices_swagger, 'r') as f:    
        doc = yaml.load(f)
        data = doc["paths"]
        for k in data.keys():
            for l in data[k].keys():
                    for m in data[k][l]["parameters"]:
                        if 'type' in m:
                            if (m["type"] == 'integer'):
                                int_type_parameters.append(m["name"])
           
        data = doc["definitions"]
        for k in data.keys():
                for l in data[k].keys(): 
                    if l == 'properties':
                        for m in data[k][l].keys():
                            for n in data[k][l][m].keys():
                                if 'type' in n:  
                                    if (data[k][l][m]["type"] == "integer"):
                                         int_type_parameters.append(m) 
                                            
        data = doc["parameters"]
        for k in data.keys():
            if 'type' in data[k]:
                if (data[k]['type'] == "integer"):
                    int_type_parameters.append(k)
                   
        return int_type_parameters
   
   
def process_Result(result):
    print "Success", result  
     
     
def process_Error(Failure):
    print "Error Occurred" , Failure
 
 
def get_func_output(methodToCall, argsdict):
    global func_dict
    f1=open(negative_testcase_log_file,"a")
    d = defer.Deferred()
    func_name = func_dict[methodToCall]
    try:
                result, http_response = methodToCall(**argsdict).result()
         
                if (result is None):
                    result_type = type(result)                
                   
                elif(type(result) is list):
                    if not result:
                        result_type = '<type \\'NoneType\\'>'
                    else:
                        for data in result:
                            if isinstance(data, unicode):
                                result_type = type(data.encode('utf8'))
                            else:
                                result_type = type(data)
                            
                elif isinstance(result, unicode):
                    result_type = type(result.encode('utf8'))
                       
                else:
                    result_type = type(result)
                        
                matches=re.findall(r'\\'(.+?)\\'',str(result_type))          
         
                print >>f1, "FunctionName:", func_name.replace('\\n',''), '&&', "HttpResponse:", http_response.status_code, "&&", "ResultType:", matches[0], '&&', "Result:", result
                reactor.callLater(1, d.callback, (http_response.status_code))#@UndefinedVariable
         
    except Exception as e:
        print >>f1, "FunctionName:", func_name.replace('\\n',''), '&&', "HttpResponse:", e.status_code, "&&", "ResultType:", "NoneType", '&&', "Result:", str(e)
        reactor.callLater(1, d.callback, str(e))#@UndefinedVariable
    return d    
     
     
 
def test_negative_scenerios(networkDevice):
    with open(negative_testfunc_file) as input_file:
        count = 0
        global func_dict
        twisted_dict = dict()
        func_dict = dict()
        for data in input_file:
         
            func_name, tag_name = data.split('&&')
            func_name = func_name.split('$')[0]
            tag_name = tag_name.replace(' ','')
            f1=open(negative_testcase_log_file,"a")
             
            argsdict, funcname = get_func_name(func_name)
             
            client_obj = 'networkDevice.'+tag_name
            methodToCall = getattr(eval(client_obj), funcname)
             
            func_dict.update({methodToCall:func_name})
            twisted_dict.update({methodToCall: argsdict})
             
        try:
            dl = DeferredList(get_func_output(methodToCall, argsdict) for methodToCall,argsdict in twisted_dict.items())
            dl.addCallback(process_Result)
            dl.addErrback(process_Error)
        except Exception as e:
            print>>f1, "Exception Occurred", str(e)
            print "Exception Occurred", str(e)  
   
""")
             
    rr = testdir.run(sys.executable, "-m", "pytest", "--twisted")
    outcomes = rr.parseoutcomes()
    assert outcomes.get("passed") == 1             
