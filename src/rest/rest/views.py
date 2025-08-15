from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json, logging, os
from pymongo import MongoClient
from datetime import datetime

mongo_uri = os.environ["MONGO_URL"]
db = MongoClient(mongo_uri)['test_db']

class TodoListView(APIView):

    def get(self, request):
        try:
            # Get all todo items from the 'todos' collection
            todos_collection = db['todos']
            todos = list(todos_collection.find({}, {'_id': 0}))  # Exclude MongoDB _id field
            
            return Response({
                'todos': todos,
                'count': len(todos)
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logging.error(f"Error fetching todos: {str(e)}")
            return Response({
                'error': 'Failed to fetch todos',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self, request):
        try:
            # Get the todo description from request data
            todo_description = request.data.get('description')
            
            if not todo_description or not todo_description.strip():
                return Response({
                    'error': 'Todo description is required'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Create todo document
            todo_doc = {
                'description': todo_description.strip(),
                'created_at': datetime.utcnow().isoformat(),
                'completed': False
            }
            
            # Insert into MongoDB
            todos_collection = db['todos']
            result = todos_collection.insert_one(todo_doc)
            
            # Return the created todo (without MongoDB _id)
            created_todo = {
                'id': str(result.inserted_id),
                'description': todo_doc['description'],
                'created_at': todo_doc['created_at'],
                'completed': todo_doc['completed']
            }
            
            return Response({
                'message': 'Todo created successfully',
                'todo': created_todo
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logging.error(f"Error creating todo: {str(e)}")
            return Response({
                'error': 'Failed to create todo',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

