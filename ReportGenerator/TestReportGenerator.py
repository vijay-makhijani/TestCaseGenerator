'''
Created on 12-Dec-2016

@author: root
'''

'''
import packages and Constants
'''
import yaml
import json
import re
from Config.Constants import negative_testcase_log_file, negative_testfunc_file, positive_testcase_log_file, positive_testfunc_file, HTMLTestReport_file, networkdevices_swagger

class TestReportGenerator(object):
     
    '''
    Find Return types of responses from Swagger file
    '''
    def find_values(self, ref, json_repr):
        results = []
        def _decode_dict(a_dict):
            try: results.append(a_dict[ref])
            except KeyError: pass
            return a_dict

        json.loads(json_repr, object_hook=_decode_dict) 
        return results        

    '''
    Find Return types of responses from Swagger file
    '''
    def get_Response_Type(self):
        with open(networkdevices_swagger, 'r') as f:    
            doc = yaml.load(f)
        data = doc["paths"]
        definitions = {}
        for k in data.keys():
            for l in data[k].keys():
                swagger_responses = data[k][l]['responses']
                func_name =  data[k][l]["operationId"]
                for m in swagger_responses.keys():
                    if(m == int(200) or m == int(204)):
                        defintion_value = self.find_values('$ref', json.dumps(swagger_responses[m]))
                        definitions[func_name] = str(defintion_value).replace('#/definitions/','')
        
        return definitions
        
    '''
    Get DataType of parameters from Swagger file
    '''
    
    def get_Parameters_Datatype(self):
        with open(networkdevices_swagger, 'r') as f:    
            doc = yaml.load(f)
    
        data = doc["definitions"]
        data_type = {}
        param = []
        for k in data.keys():
            if 'type' in data[k]:
                data_type[k] = data[k]['type']
            for l in data[k].keys():
                if l == 'properties':
                    for m in data[k][l].keys():
                        for n in data[k][l][m].keys():
                            if 'type' in n:
                                param.append(data[k][l][m]["type"])
                                data_type[m] = data[k][l][m]["type"]



        data = doc["paths"]
        for k in data.keys():
            for l in data[k].keys():
                    for m in data[k][l]["parameters"]:
                        if 'type' in m:
                            data_type[m["name"]] = m["type"]


        data = doc["parameters"]
        for k in data.keys():
            if 'type' in data[k]:
                data_type[data[k]['name']] = data[k]['type']
        
        return data_type
        
                
    '''
    Verify Negative TestCase Results
    '''
    def get_negative_scenerio_results(self, definitions, data_types):
        f = open(negative_testcase_log_file, 'r')
        f1 = open(negative_testfunc_file, 'r')
        negative_scenerio_results = {}
        for line in f:
            if line.strip():
                funcname, httpresponse, resulttype, result = line.strip().split('&&')
                httpresponse_key, httpresponse_value = httpresponse.strip().split(':')
                resulttype_key, resulttype_value = resulttype.strip().split(':')
                funcname_key, funcname_value = funcname.strip().split(':', 1)
                result_key, result_value = result.strip().split(':')
                if (httpresponse_value.replace(' ', '') == '400'):
                    negative_scenerio_results[funcname_value] = "pass"
                else:
                    negative_scenerio_results[funcname_value] = "fail"
        print("Negative Test Case Scenerios")
        for keys,values in negative_scenerio_results.items():
            print(keys.replace(' ', ''), values)
        return negative_scenerio_results
        f.close()
        f1.close()
        

    '''
    Verify Positive TestCase Results
    '''
    def get_positive_scenerio_results(self, definitions, data_type):
        f = open(positive_testcase_log_file, 'r')
        f1 = open(positive_testfunc_file, 'r')
        positive_scenerio_results = {}
        for line in f:
            if line.strip():
                funcname, httpresponse, resulttype, result = line.strip().split('&&')
                httpresponse_key, httpresponse_value = httpresponse.strip().split(':')
                resulttype_key, resulttype_value = resulttype.strip().split(':')
                funcname_key, funcname_value = funcname.strip().split(':', 1)
                result_key, result_value = result.strip().split(':')
        
                if 'bravado_core.model' in resulttype_value:
                    resulttype_value = 'object'
        
                key = funcname_value.split('(')[0]
                func = definitions.get(key.replace(' ',''))
                matches=re.findall(r'\'(.+?)\'',str(func))
                if len(matches) > 0:
                    datatype = data_type.get(matches[0])
                else:
                    datatype = "NoneType"
            
                if (httpresponse_value.replace(' ', '') == '200' or httpresponse_value.replace(' ', '') == '201' or httpresponse_value.replace(' ', '') == '204' or httpresponse_value.replace(' ', '') == '404'):
                    if (httpresponse_value.replace(' ', '') == '200'):
                
                        if(result_value.replace(' ','') == "[]"):
                            positive_scenerio_results[funcname_value] = "pass"
                            continue

                        if(resulttype_value.replace(' ', '') in datatype.replace(' ', '')):
                            f1 = open(positive_testfunc_file, 'r')
                            for func_comp_line in f1:
                                func_line, tag_name = func_comp_line.split('&&')
                                if funcname_value.replace(' ','')+"$" in func_line:
                                    expected_value = func_line.split("$")[1]
                                    if(expected_value.replace(' ','') == result_value.replace(' ','')):
                                        positive_scenerio_results[funcname_value] = "pass"
                                    else:
                                        positive_scenerio_results[funcname_value] = "fail"
                                 
                                else:
                                    positive_scenerio_results[funcname_value] = "pass"
                        else:
                            positive_scenerio_results[funcname_value] = "fail"
                    else:
                        positive_scenerio_results[funcname_value] = "pass"
                else:
                    positive_scenerio_results[funcname_value] = "fail"
            
        print("Positive Test Case Scenerios")
        for keys,values in positive_scenerio_results.items():
            print(keys.replace(' ', ''), values)       
            
        return positive_scenerio_results
        f.close()
        f1.close()



    '''
    Generate HTML Report
    '''
    def generate_HTML_Report(self, positive_scenerio_results,negative_scenerio_results):
        outfile = open(HTMLTestReport_file, "w")
        print>>outfile, """<html>
        <head>
            <title>API Test Information</title>
        </head>
        <body>
        <table border="1">"""
 
        print>>outfile, "<tr bgcolor=grey><th>TestCase</th><th>Result</th></tr>"
 
        for keys,values in positive_scenerio_results.items():
            if(values == "pass"):
                print>>outfile, "<tr bgcolor=#2EFE2E><td>%s</td><td>%s</td></tr>" % (
                    keys.replace(' ', ''), values)
            else:
                print>>outfile, "<tr bgcolor=#FE2E2E><td>%s</td><td>%s</td></tr>" % (
                    keys.replace(' ', ''), values)
        
        for keys,values in negative_scenerio_results.items():
            if(values == "pass"):
                print>>outfile, "<tr bgcolor=#2EFE2E><td>%s</td><td>%s</td></tr>" % (
                    keys.replace(' ', ''), values)
            else:
                print>>outfile, "<tr bgcolor=#FE2E2E><td>%s</td><td>%s</td></tr>" % (
                    keys.replace(' ', ''), values)
                
        print>>outfile, """</table>
        </body></html>"""  


'''
Verify the results of positive and negative scenerios and generate HTML Report
'''

obj = TestReportGenerator()
definitions = obj.get_Response_Type()
data_types = obj.get_Parameters_Datatype()
negative_scenerio_results = obj.get_negative_scenerio_results(definitions,data_types)
positive_scenerio_results = obj.get_positive_scenerio_results(definitions,data_types)
obj.generate_HTML_Report(positive_scenerio_results,negative_scenerio_results)
