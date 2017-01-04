'''
Created on 30-Nov-2016

@author: vijay.m
'''
project_path = "/opt/AutomationWorkSpace/GenericTestCaseGenerator"
negative_testcase_log_file = project_path+"/TestBuilder/output_files/negative_testcase_log_file"
positive_testcase_log_file = project_path+"/TestBuilder/output_files/positive_testcase_log_file"
negative_testfunc_file = project_path+"/SwaggerParser/output_files/negative_testfunc_file"
positive_testfunc_file = project_path+"/SwaggerParser/output_files/positive_testfunc_file"
HTMLTestReport_file = project_path+"/ReportGenerator/output_files/HTMLTestReport.html"
#swaggerFile = project_path+"/SwaggerConnexion_nbtlpc/nbtlpc.yaml"
swaggerFile = project_path+"/SwaggerConnexion/networkdevices_swagger.yaml"

scenerio_list = ['positive','negative']
value_type_list = ['lower_boundary', 'upper_boundary', 'random']