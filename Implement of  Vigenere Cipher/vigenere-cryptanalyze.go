package main

import (
	"fmt"
	"io/ioutil"
	"os"
	"strconv"
)


func m_cal(s string, length int) float32 {
	var (
		begin_int int = int('A')
		probability = []float32 {0.082, 0.015, 0.028, 0.043, 0.127, 0.022, 0.02, 0.061, 0.07, 0.002, 0.008,
	0.04, 0.024, 0.067, 0.075, 0.019, 0.001, 0.06, 0.063, 0.091, 0.028, 0.01, 0.023, 0.001, 0.02, 0.001,}
		m float32 = 0.0
	)
	for l := 0; l < 26; l++ {
		f := 0
		for i := 0; i < len(s); i++ {
			if int(s[i]) == begin_int+l {
				f += 1
			}
		}
		m += probability[l] * float32(f)
		//fmt.Println(string(rune(begin_int+l)),float32(f))
	}


	return m / float32(length)
}

func main(){
	var (

		filename string = os.Args[1]
		key_len,_ = strconv.Atoi(os.Args[2])
		matrix []string
		m float32

		guess_key string = ""
		//guess_l rune

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
		for step := 1; step < 26; step++ {
			length := 0
			s := ""
			for i := 0; i < len(matrix[col]); i++{
				if matrix[col][i] < 'A' || matrix[col][i] > 'Z' {
					break
				}
				length ++
				i_0 := int(matrix[col][i])
				i_1 := i_0 + step
				if i_1 > int(end_char) {
					i_1 = int(begin_char) + i_1 - int(end_char) - 1
				}
				c := rune(i_1)
				s += string(c)
			}
			m = m_cal(s, length)
			//fmt.Println(s)
			if m >= 0.055 {
				guess_key += string(rune(int('A') + 26 - step))
				//fmt.Println(m, guess_key, step, length)
				break
			}

		}
		//fmt.Println(col, m, guess_key)
	}
	fmt.Println(guess_key)

}
