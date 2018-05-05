"""XML generator from file.json"""


__author__ = 'Hugo Barzano'
__date__ = '2017/2018'
__version__ = 'v1.0'
__credits__ = 'GAC'
__file__ = 'generator.py'

import json
import xmltodict
import sys
import os
import getopt

def readInput(input_file):
    """Function to read input files.
         :param input_file: input file path"""
    print "Reading input file from "+input_file
    try:
        with open(input_file, 'r') as f:
    	       input_file_as_string = f.read()
        return input_file_as_string
    except EnvironmentError:
        print("Oops! Error Reading input file...")
        exit()

def writeOutput(output_file,output_string):
    """Function to write output files.
         :param output_file: output file path
         :param output_string: string to write in the output file"""
    print "Writing output file in "+output_file
    try:
        with open(output_file, 'w') as f:
    	       f.write(output_string)
    except EnvironmentError:
        print("Oops! Error writing output file...")
        exit()

def validateJson(input_string):
    """"Function to validate json inputs.
         :param input_string: json as string to validate"""
    try:
        validate_input=json.loads(input_string)
        print "Valid structure of input json file..."
    except ValueError:
        print("Oops! Invalid structure of input json file...")
        exit()

def parseInputJsonToXML(input_string):
    """Function to parse json files as input to XML string.
         :param input_string: input data file as string """
    xmlString = xmltodict.unparse(json.loads(input_string), pretty=True)
    return xmlString

def parseInputXMLToJson(input_string):
    """Function to parse xml files as input to json string.
         :param input_string: input data file as string """
    jsonString = json.dumps(xmltodict.parse(input_string))
    return jsonString

def usage():
    """Method to display generator usage. """
    print """
Usage: python generador.py [options]

Options
-v, --version			Show the version of this script
-h, --help			Show this help.
-i <path>, --input <path>    	Input file
-o <path>, --output <path>     	Output file
-d,         --debug         	Debug Mode
"""

def version():
    """Function to display software version"""
    print "version 1.0"

def main(argv):
    """Main method to execute the generator.
                :param argv: value from 0 to n-1 to ident"""
    input_file=None
    output_file=None
    debug=False

    # process arguments
    try:
        opts, args = getopt.getopt(argv, "hvi:o:d", ["help", "version", "input=","output=","debug"])
    except getopt.GetoptError as err:
        print str(err)
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-v", "--version"):
            version()
            sys.exit()
        elif opt in ("-i", "--input"):
            input_file = arg
        elif opt in ("-o","--output"):
            output_file=arg
        elif opt in ("-d", "--debug"):
            debug = True
            print "Debug: TRUE"
        else:
            usage()
            sys.exit()

    print "GAC: P1 - GENERATOR"
    if debug:
        print "INPUT: "+ input_file
        print "OUTPUT: "+ output_file



    input_as_string=readInput(input_file)
    if debug: print input_as_string
    if input_file.split(".")[1]=="json":
        print "PROCESSING --> JSON 2 XML "
        if debug: print "Validating json input file structure..."
        validateJson(input_as_string)
        if debug: print "Serializing output file format..."
        if not ".xml" in output_file: output_file=output_file+".xml"
        output_as_string=parseInputJsonToXML(input_as_string)
    elif input_file.split(".")[1]=="xml":
        print "PROCESSING --> XML 2 JSON"
        if debug: print "Serializing output file format"
        if not ".json" in output_file: output_file=output_file+".json"
        output_as_string=parseInputXMLToJson(input_as_string)
    else:
        print "Invalid input file format. It should be input.json or input.xml "
        exit()
    writeOutput(output_file,output_as_string)
    if debug:print output_as_string


# --------------------------------------------------------------------------------------------------
# Main exec
# --------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1:])
    else:
        usage()
        sys.exit()
