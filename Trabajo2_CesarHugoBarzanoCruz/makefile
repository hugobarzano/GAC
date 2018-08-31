#Makefile

doc:
	rm -rf software_specification && mkdir software_specification && pydoc -w ./ && mv ./*.html software_specification/

init:
	python init.py

testCase1:
	sh TestCase_1.sh

testCase2:
	sh TestCase_2.sh

testCase3:
	sh TestCase_3.sh

testCase4:
	sh TestCase_4.sh

testCase5:
	sh TestCase_5.sh

testCaseError1:
	sh TestCase_6.sh

clean:
		rm ./output/*
