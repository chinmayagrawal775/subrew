import React, { useState, useEffect } from 'react';
import './App.css';
import logo from './logo.svg';

export function App() {
  const [todos, setTodos] = useState([]);
  const [newTodo, setNewTodo] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  // Fetch todos from the API
  const fetchTodos = async () => {
    try {
      setLoading(true);
      setError('');
      const response = await fetch('http://localhost:8000/todos/');
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      setTodos(data.todos || []);
    } catch (err) {
      console.error('Error fetching todos:', err);
      setError('Failed to fetch todos. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Create a new todo
  const createTodo = async (description) => {
    try {
      setLoading(true);
      setError('');
      
      const response = await fetch('http://localhost:8000/todos/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ description }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      console.log('Todo created:', data);
      
      // Refresh the todo list after creating a new todo
      await fetchTodos();
      
      // Clear the form
      setNewTodo('');
    } catch (err) {
      console.error('Error creating todo:', err);
      setError(err.message || 'Failed to create todo. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    if (newTodo.trim()) {
      createTodo(newTodo.trim());
    }
  };

  // Fetch todos on component mount
  useEffect(() => {
    fetchTodos();
  }, []);

  return (
    <div className="App">
      <div>
        <h1>List of TODOs</h1>
        {todos.length === 0 && !loading ? (
          <p>No todos found. Create your first todo!</p>
        ) : (
          <ul>
            {todos.map((todo, index) => (
              <li key={todo.id || index}>
                {todo.description}
                <span style={{ fontSize: '0.8em', color: 'gray', marginLeft: '10px' }}>
                  {new Date(todo.created_at).toLocaleString()}
                </span>
              </li>
            ))}
          </ul>
        )}
        {loading && <p>Loading...</p>}
        {error && <p style={{ color: 'red' }}>{error}</p>}
      </div>
      <div>
        <h1>Create a ToDo</h1>
        <form onSubmit={handleSubmit}>
          <div>
            <label htmlFor="todo">ToDo: </label>
            <input 
              type="text" 
              id="todo"
              value={newTodo}
              onChange={(e) => setNewTodo(e.target.value)}
              disabled={loading}
              placeholder="Enter your todo description"
            />
          </div>
          <div style={{"marginTop": "5px"}}>
            <button type="submit" disabled={loading || !newTodo.trim()}>
              {loading ? 'Adding...' : 'Add ToDo!'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default App;
