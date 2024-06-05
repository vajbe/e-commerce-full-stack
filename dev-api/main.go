package main

import (
	"context"
	"fmt"
	"log"
	"net/http"
	"os"

	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
)

func helloHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "Hello, World!")
}

func main() {

	mongoURL := os.Getenv("MONGO_URL")

	clientOptions := options.Client().ApplyURI(mongoURL)

	_, err := mongo.Connect(context.TODO(), clientOptions)

	if err != nil {
		log.Printf("Failed to connect to DB %s", err)
	} else {
		log.Print("Connected to DB")
	}

	/* 	defer func() {
		if err := client.Disconnect(context.TODO()); err != nil {
			log.Print("Failed to disconnect from DB")
		}
	}() */

	http.HandleFunc("/", helloHandler)
	fmt.Println("Server is running on port 8080...")
	http.ListenAndServe(":8080", nil)
}
