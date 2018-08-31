package main

import (
	"encoding/json"
	"fmt"
	_ "github.com/go-sql-driver/mysql"
	"io/ioutil"
	"os"
	"strings"
	//"github.com/jinzhu/gorm"
	// _ "database/sql"
	// "database/sql"
	"bytes"

	"database/sql"

	"strconv"
)


const PYTHON_TEMPLATE_PATH="./input/template.py"
const OUTPUT_CODE_PATH = "./output/"

type SGBD struct {
	User     string `json:"user"`
	Password string `json:"password"`
	Host     string `json:"host"`
	DB       string `json:"database"`
	Table    string `json:"table"`
	Model    string `json:"model_name"`
}

func LoadConfig(file_path string) map[string]SGBD {
	file_config, err := ioutil.ReadFile(file_path)
	if err != nil {
		fmt.Println("Error reading config file")
		fmt.Println(err.Error())
		os.Exit(1)
	}
	fmt.Println(file_config)
	var config_Data map[string]SGBD
	err2 := json.Unmarshal(file_config, &config_Data)
	if err2 != nil {
		fmt.Println("Error unmarshaling config file")
		fmt.Println(err2.Error())
		os.Exit(1)
	}
	return config_Data
}

type Result struct {
	Field   string
	Type    string
	Null    sql.NullString
	Key     sql.NullString
	Default sql.NullString
	Extra   sql.NullString
}

func checkErr(err error) {
	if err != nil {
		panic(err.Error())
	}
}

func GenerateInit(atributes []Result) string {
	var init bytes.Buffer
	init.WriteString("def __init__(self")
	//init.WriteString()
	for index := range atributes {
		fmt.Printf("Atr: %s  tipe: %s \n", atributes[index].Field, atributes[index].Type)
		init.WriteString(", ")
		init.WriteString(atributes[index].Field)
		init.WriteString("=None")
	}
	init.WriteString("):\n")
	init.WriteString("\n")
	for index := range atributes {
		init.WriteString("	")
		init.WriteString("	")
		init.WriteString("self.")
		init.WriteString(atributes[index].Field)
		init.WriteString("=")
		init.WriteString(atributes[index].Field)
		init.WriteString("\n")
	}

	fmt.Print(init.String())
	return init.String()
}

func WriteCodeClass(input string, output string) {

	file, err := os.Create(output)
	checkErr(err)
	bytesNun, err := file.WriteString(input)
	checkErr(err)
	fmt.Printf("Wrote %d bytes\n", bytesNun)
	file.Sync()
}

func GenerateCrud(atributes []Result, connection SGBD) {
	for t := range atributes {
		fmt.Printf(strconv.Itoa(t))
		fmt.Printf(atributes[t].Type)
	}
	var file []byte
	file, err := ioutil.ReadFile(PYTHON_TEMPLATE_PATH)

	if err != nil {
		checkErr(err)
	}

	code := strings.Replace(string(file), "<user>", connection.User, 1)
	code = strings.Replace(code, "<password>", connection.Password, 1)
	if strings.Compare(connection.Host, "") == 0 {
		code = strings.Replace(code, "<host>", "127.0.0.1", 1)
	} else {
		code = strings.Replace(code, "<host>", connection.Host, 1)
	}
	code = strings.Replace(code, "<database>", connection.DB, 1)
	code = strings.Replace(code, "<table>", connection.Table, 1)

	model_name := ""
	if len(connection.Model) == 0 {
		model_name = strings.Title(connection.Table)
	} else {
		model_name = strings.Title(connection.Model)
	}
	code = strings.Replace(code, "<Model>", model_name, -1)
	//fmt.Printf(string(file))
	init := GenerateInit(atributes)
	code = strings.Replace(code, "<init>", init, 1)
	WriteCodeClass(code, OUTPUT_CODE_PATH+model_name+"_class_generated.py")
	//fmt.Printf(code)
}

func GetMysqlTableStruct(connection SGBD) []Result {
	var data_connection bytes.Buffer
	data_connection.WriteString(connection.User)
	data_connection.WriteString(":")
	data_connection.WriteString(connection.Password)
	data_connection.WriteString("@")
	data_connection.WriteString(connection.Host)
	data_connection.WriteString("/")
	data_connection.WriteString(connection.DB)
	fmt.Println(data_connection.String())
	db, err := sql.Open("mysql", data_connection.String())
	if err != nil {
		panic(err.Error()) // Just for panic
	}
	defer db.Close()
	// query
	rows, err := db.Query("DESCRIBE "+ connection.Table)
	checkErr(err)

	var result Result
	var atributes []Result

	for rows.Next() {
		err = rows.Scan(&result.Field, &result.Type, &result.Null, &result.Key, &result.Default, &result.Extra)
		checkErr(err)
		atributes = append(atributes, result)
	}

	return atributes
}

func main() {
	var CONFIG_PAHT string = os.Getenv("GENERATOR_CONFIG")
	var config_data = LoadConfig(CONFIG_PAHT)

	for sgbd := range config_data {
		fmt.Printf("SGBD: '%s' \n user: '%s' \n pass: '%s'\n host: '%s'\n database: '%s' \n", sgbd, config_data[sgbd].User, config_data[sgbd].Password, config_data[sgbd].Host, config_data[sgbd].DB)
		if strings.Contains(sgbd, "mysql") {
			fmt.Println("MYSQL SGBD")
			atributes := GetMysqlTableStruct(config_data[sgbd])
			GenerateCrud(atributes, config_data[sgbd])
		} else if strings.Contains(sgbd, "postgres") {
			fmt.Println("Postgres SGBD TBD")
		} else if strings.Contains(sgbd, "sqlite3") {
			fmt.Println("SQLite3 SGBD TBD")
		} else if strings.Contains(sgbd, "mongo") {
			fmt.Println("MONGO SGBD TBD")
		} else {
			fmt.Println("Not supported SGBD")
		}
	}
}
