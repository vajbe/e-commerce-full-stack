package main

import (
	"context"
	"os"

	"go.mongodb.org/mongo-driver/mongo"
	"go.mongodb.org/mongo-driver/mongo/options"
	"go.mongodb.org/mongo-driver/mongo/readpref"
)

func GetDBConnection() (*mongo.Client, error) {
	mongoURL := os.Getenv("MONGO_URL")
	clientOptions := options.Client().ApplyURI(mongoURL)
	client, err := mongo.Connect(context.Background(), clientOptions)
	if err != nil {
		return nil, err
	}
	// Ping the database to verify the connection
	if err := client.Ping(context.Background(), readpref.Primary()); err != nil {
		return nil, err
	}
	return client, nil
}
