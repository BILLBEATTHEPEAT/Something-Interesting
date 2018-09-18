package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strings"
)


func main(){

	var (
		en_key string = os.Args[1]
		filename string = os.Args[2]
		begin_char rune = 'A'
		end_char rune = 'Z'
	)


	for i:=0;i<len(en_key);i++ {
		if strings.Compare(string(en_key[i]), "A") >= 0 && strings.Compare(string(en_key[i]), "Z") <= 0 {
			continue
		} else {
			fmt.Println("The key should consist of uppercase letters")
			return
		}
	}
	if len(en_key) > 32 {
		fmt.Println("The key should consist of letters up to 32 characters")
		return
	}

	buf, err := ioutil.ReadFile(filename)
	if err != nil {
		fmt.Fprintf(os.Stderr, "File Error: %s\n", err)
	}
	//fmt.Printf("%s\n", string(buf))
	input := string(buf)


	//var input string = "ATTAC1111--,,"+string('\n')+"KATDAWN"

	var output string
	key := 0

	for i:=0; i<len(input);i++ {
		if input[i] == '\n' {
			output += string('\n')
			continue
		}
		if (input[i] < 'a' || input[i] > 'z') && (input[i] < 'A' || input[i] > 'Z') {
			continue
		}
		i_0 := int(input[i])
		i_1 := i_0 + (int(en_key[key]) - int(begin_char))
		if i_1 > int(end_char){
			i_1 = int(begin_char) + i_1 - int(end_char) - 1
		}
		c := rune(i_1)
		output += string(c)

		key += 1
		if key == len(en_key){
			key = 0
		}
	}
	//fmt.Println(en_key, filename)
	fmt.Println(output)
	buf = []byte(output)
	err = ioutil.WriteFile("Ciphertext.txt", buf, 0644)
	if err != nil {
		panic(err.Error())
	}
}