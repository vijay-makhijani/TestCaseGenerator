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
networkdevices_swagger = project_path+"/SwaggerConnexion/networkdevices_swagger.yaml"

invalid_devices = ["dsak*463@90", "sdk^&%kjshsd", "#gfdsadfk09"]
devices = ["Switch", "Router", "Hub", "Gateway", "NIC", "Bridge", "Modem", "KeyBoard", "Mouse", "Monitor"]
devices_type = ["Peripheral", "Network"]
scenerio_list = ['positive','negative']