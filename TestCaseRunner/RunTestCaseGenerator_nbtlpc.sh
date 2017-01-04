#!/bin/bash

current_dir=$(pwd)
testcaseRunner=$current_dir/TestCaseRunner
swaggerParser=$current_dir/SwaggerParser
restService=$current_dir/SwaggerConnexion_nbtlpc
testBuilder=$current_dir/TestBuilder
reportGenerator=$current_dir/ReportGenerator

Start_DeviceRestService()
{
	echo "-------- Starting Rest Service --------"
	restServiceProcess=`ps -aux | grep app.py | grep -v grep | awk '{ print $2 }'`
	if [[ ! -z $restServiceProcess ]]
	then
		kill -9  $restServiceProcess
	fi
	$restService/app.py &
	sleep 5
}


Parse_DeviceSwagger()
{
	echo "-------- Parsing Swagger File and generating functions --------"
	python $swaggerParser/DeviceSwaggerParser.py
	echo "########## Function Files are #########"
	echo $swaggerParser/output_files/positive_testfunc_file
	echo $swaggerParser/output_files/negative_testfunc_file
}

Run_TestScenerios_PytestTwisted()
{
	echo "-------- Run Positive and Negative Test Scenerios using Bravado, Pytest and Twisted --------"
	pytest $testBuilder/pytest/Twisted_Test_APIServices.py
	echo "########## Output Files are #########"l
	echo $testBuilder/output_files/positive_testcase_log_file
	echo $testBuilder/output_files/negative_testcase_log_file	
}

ValidateResults_GenerateReport()
{
	echo "-------- Verify responses of the Rest Service with Swagger file and Generate the Test Report --------"
	python $reportGenerator/TestReportGenerator.py
	echo "########## HTML Test Report Location #########"l
	echo $reportGenerator/output_files/HTMLTestReport.html
}


if [ $# -lt 1 -o $# -gt 2 ]
then
	echo "Usage- scriptname auto  or scriptname manual first  or scriptname manual second"
	exit
	
elif ([ "$1" == "auto" ])
then
	Start_DeviceRestService
	Parse_DeviceSwagger
	Run_TestScenerios_PytestTwisted
	ValidateResults_GenerateReport
	
elif ([ "$1" == "manual" ] && [ "$2" == "first" ])
then 
	Start_DeviceRestService
	Parse_DeviceSwagger
	
elif ([ "$1" == "manual" ] && [ "$2" == "second" ])
then
	Run_TestScenerios_PytestTwisted
	ValidateResults_GenerateReport
	
else
	echo "Invalid Arguments"
	echo "Usage- scriptname auto  or scriptname manual first  or scriptname manual second"
fi





