package main

import (
	"fmt"
	"log"
	"net/http"
)

func main() {

	_, err := GetDBConnection()

	if err != nil {
		log.Printf("Failed to connect to DB %s", err)
	} else {
		log.Print("Connected to DB")
	}

	http.HandleFunc("/api/login", Login)
	fmt.Println("Server is running on port 8080...")
	http.ListenAndServe(":8080", nil)
}
