package main

import (
	"context"
	"encoding/json"
	"log"
	"net/http"

	"go.mongodb.org/mongo-driver/bson"
	"go.mongodb.org/mongo-driver/mongo/options"
)

type UserLogin struct {
	Username string `json:"username" bson:"username"`
	Password string `json:"password" bson:"password"`
}

func Login(w http.ResponseWriter, r *http.Request) {
	Method := r.Method

	switch Method {
	case "POST":
		{
			decoder := json.NewDecoder(r.Body)
			var t UserLogin
			err := decoder.Decode(&t)
			if err != nil {
				log.Printf("Error: %s", err)
				return
			}

			client, err := GetDBConnection()
			if err != nil {
				log.Printf("Error: %s", err)
			}

			log.Printf("Received a request")

			var result bson.M
			users := client.Database("ecommerce").Collection("users")
			opts := options.FindOne().SetSort(bson.D{{Key: "email", Value: 1}})
			err = users.FindOne(context.Background(), bson.D{{Key: "email", Value: t.Username}}, opts).Decode(&result)
			if err != nil {
				log.Printf("Error: %s", err)
			}
			log.Printf("Found this username")
		}
	}
}
