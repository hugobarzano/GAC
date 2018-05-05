#Makefile

doc:
	rm -r software_specification && mkdir software_specification && pydoc -w ./ && mv ./*.html software_specification/

testString:
	python generator.py -i input/testString.json -o output/testString.xml -d

testNumbers:
	python generator.py -i input/testNumbers.json -o output/testNumbers.xml -d

testObjects:
	python generator.py -i input/testObjects.json -o output/testObjects.xml -d

testBoolean:
		python generator.py -i input/testBoolean.json -o output/testBoolean.xml -d

testNull:
		python generator.py -i input/testNull.json -o output/testNull.xml -d

testArrays:
	python generator.py -i input/testArrays.json -o output/testArrays.xml -d

testServlet:
	python generator.py -i input/servlet.json -o output/output_testservlet.xml -d

testXML2JSON:
		python generator.py -i input/testXML2JSON.xml -o output/output_testXML2JSON.json -d

testBadInputFormat:
		python generator.py -i input/input.format -o output/output_testBadInputFormat.xml -d

testMissingInputFile:
		python generator.py -i input/missing_file -o output/output_testmissingfile.xml -d

testBadJson:
		python generator.py -i input/badInput.json -o output/output_testBAdInput.xml -d
