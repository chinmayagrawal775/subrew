from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import logging
from typing import Dict, Any
from pymongo import MongoClient
from datetime import datetime
import os
from bson import ObjectId

mongo_uri = os.environ["MONGO_URL"]
db = MongoClient(mongo_uri)['test_db']


class TodoService:
    """Service layer for todo operations"""
    
    def __init__(self, db):
        self.db = db
        self.todos_collection = db['todos']
    
    def get_all_todos(self):
        """Get all todos from database"""
        try:
            todos = list(self.todos_collection.find({}, {'_id': 0}))
            return todos
        except Exception as e:
            logging.error(f"Error fetching todos: {str(e)}")
            raise
    
    def create_todo(self, description):
        """Create a new todo"""
        try:
            if not description or not description.strip():
                raise ValueError("Todo description is required")
            
            todo_doc = {
                'description': description.strip(),
                'created_at': datetime.utcnow().isoformat(),
                'completed': False
            }
            
            result = self.todos_collection.insert_one(todo_doc)
            
            created_todo = {
                'id': str(result.inserted_id),
                'description': todo_doc['description'],
                'created_at': todo_doc['created_at'],
                'completed': todo_doc['completed']
            }
            
            return created_todo
        except Exception as e:
            logging.error(f"Error creating todo: {str(e)}")
            raise


# Service instance
todo_service = TodoService(db)


class TodoListView(APIView):
    """View for handling todo list operations"""

    def get(self, request):
        """Get all todos"""
        try:
            todos = todo_service.get_all_todos()
            return Response({
                'todos': todos,
                'count': len(todos)
            }, status=status.HTTP_200_OK)
        except Exception as e:
            logging.error(f"Error in get todos: {str(e)}")
            return Response({
                'error': 'Failed to fetch todos',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def post(self, request):
        """Create a new todo"""
        try:
            description = request.data.get('description')
            if not description or not description.strip():
                return Response({
                    'error': 'Todo description is required'
                }, status=status.HTTP_400_BAD_REQUEST)
                
            todo = todo_service.create_todo(description)
            
            return Response({
                'message': 'Todo created successfully',
                'todo': todo
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            logging.error(f"Error creating todo: {str(e)}")
            return Response({
                'error': 'Failed to create todo',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

