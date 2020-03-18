package main

import (
	"config"
	"fmt"
)

func main() {
	config.LoadConfig()
	fmt.Println("Hello Prac_Proj!")
}
