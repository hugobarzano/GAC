#Makefile

doc:
	rm -r software_specification && mkdir software_specification && pydoc -w ./ && mv ./*.html software_specification/

init:
	echo "INIT"

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

testBadInputFormat:
		python generator.py -i input/input.format -o output/output_testBadInputFormat.xml -d

testMissingInputFile:
		python generator.py -i input/missing_file -o output/output_testmissingfile.xml -d

clean:
		rm ./output/*
