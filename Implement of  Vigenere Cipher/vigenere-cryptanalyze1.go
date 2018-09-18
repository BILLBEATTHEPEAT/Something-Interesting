package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
)

func f_cal(s string) rune {
	var (
		begin_int int = int('A')
		fmax int = 0
		l_most rune= 'A'
	)
	for l := 0; l < 26; l++ {
		f := 0
		for i := 0; i < len(s); i++ {
			if int(s[i]) == begin_int+l {
				f += 1
			}
		}
		if f > fmax {
			fmax = f
			l_most = rune(begin_int+l)
		}
	}

	return l_most
}

func main(){
	var (

		filename string = os.Args[1]
		key_len,_ = strconv.Atoi(os.Args[2])
		matrix []string

		guess_key string = ""
		guess_l rune

		begin_char rune = 'A'
		end_char rune = 'Z'
	)

	buf, err := ioutil.ReadFile(filename)
	if err != nil {
		fmt.Fprintf(os.Stderr, "File Error: %s\n", err)
	}
	//fmt.Printf("%s\n", string(buf))
	input := string(buf)


	for i := 0; i < key_len; i++ {
		column := ""
		for j := 0; j < (len(input)/key_len+1); j++ {
			if (j*key_len+i) < len(input){
				column += string(input[j*key_len+i])
			} else {
				column += "_"
			}
		}
		matrix = append(matrix, column)
	}


	for col := 0; col < key_len; col++ {

		l := f_cal(matrix[col])
		if int(l) < int('E') {
			guess_l = rune(int(l) + int(end_char) - int('E') + 1)
		} else {
			guess_l = rune(int(l) - int('E') + int(begin_char))
		}
		guess_key += string(guess_l)
	}
	fmt.Println(guess_key)

}

