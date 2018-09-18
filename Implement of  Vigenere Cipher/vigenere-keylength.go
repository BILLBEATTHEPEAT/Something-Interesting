package main

import (
	"fmt"
	"io/ioutil"
	"math"
	"os"
)

func ic_cal(s string) float32 {
	var (
		begin_int int = int('A')
		numerator float32 = 0.0
		dominator float32 = float32(len(s)*(len(s)-1))/26
	)
	for l := 0; l < 26; l++ {
		ni := 0
		for i := 0; i < len(s); i++ {
			if int(s[i]) == begin_int+l {
				ni += 1
			}
		}
		numerator += float32(ni*(ni-1))
	}

	return numerator/dominator
}

func main(){
	var (
		guess_len int = 1
		ic_max float32 = 1.0
		filename string = os.Args[1]
		//begin_char rune = 'A'
		//end_char rune = 'Z'
	)

	buf, err := ioutil.ReadFile(filename)
	if err != nil {
		fmt.Fprintf(os.Stderr, "File Error: %s\n", err)
	}
	//fmt.Printf("%s\n", string(buf))
	input := string(buf)

	for try_len := 1; try_len <= 20; try_len++ {

		var (
			ic float32 = 0.0
			matrix []string
		)
		//for i:=0; i < (len(input)/try_len+1); i++{
		//	if (i+1)*try_len < len(input){
		//		matrix = append(matrix, string(input[i*try_len:(i+1)*try_len]))
		//	} else {
		//		matrix = append(matrix, string(input[i*try_len:])+strings.Repeat("X", (i+1)*try_len-len(input)))
		//	}
		//}

		for i := 0; i < try_len; i++ {
			column := ""
			for j := 0; j < (len(input)/try_len+1); j++ {
				if (j*try_len+i) < len(input){
					column += string(input[j*try_len+i])
				} else {
					column += "_"
				}
			}
			matrix = append(matrix, column)
		}

		for i:=0; i < try_len; i++ {
			ic += ic_cal(matrix[i])
		}
		ic = ic / float32(try_len)

		if ic > ic_max {
			if try_len % guess_len != 0 || guess_len == 1 || math.Abs(float64(ic_max - 1.73)) >= 0.1{
				guess_len = try_len
			}
			ic_max = ic
		}
		//fmt.Println(ic, try_len, guess_len, try_len%guess_len!=0)


	}
	fmt.Println(guess_len)
}

