import React, { useState, useEffect } from 'react';
import {
  Box,
  Container,
  TextField,
  Button,
  Typography,
  Card,
  CardContent,
  IconButton,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  CircularProgress,
  Alert,
  AppBar,
  Toolbar,
  Avatar,
  Menu,
  MenuItem,
} from '@mui/material';
import {
  Add as AddIcon,
  SmartToy as AIIcon,
  Delete as DeleteIcon,
  Edit as EditIcon,
  CheckCircle as CheckIcon,
  Person as PersonIcon,
  Logout as LogoutIcon,
} from '@mui/icons-material';
import { useAuth } from '../contexts/AuthContext';
import { apiService } from '../services/api';
import { Todo, AIPlanningResponse } from '../types';

const TodoApp: React.FC = () => {
  const { user, logout } = useAuth();
  const [todos, setTodos] = useState<Todo[]>([]);
  const [newTodo, setNewTodo] = useState('');
  const [loading, setLoading] = useState(false);
  const [aiLoading, setAiLoading] = useState(false);
  const [aiDialogOpen, setAiDialogOpen] = useState(false);
  const [aiPlan, setAiPlan] = useState<AIPlanningResponse | null>(null);
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);

  useEffect(() => {
    fetchTodos();
  }, []);

  const fetchTodos = async () => {
    try {
      setLoading(true);
      const data = await apiService.getTodos();
      setTodos(data);
    } catch (error) {
      console.error('Error fetching todos:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleAddTodo = async () => {
    if (!newTodo.trim()) return;

    try {
      const todo = await apiService.createTodo({
        title: newTodo.trim(),
        priority: 'medium',
      });
      setTodos([todo, ...todos]);
      setNewTodo('');
    } catch (error) {
      console.error('Error creating todo:', error);
    }
  };

  const handleDeleteTodo = async (id: number) => {
    try {
      await apiService.deleteTodo(id);
      setTodos(todos.filter(todo => todo.id !== id));
    } catch (error) {
      console.error('Error deleting todo:', error);
    }
  };

  const handleToggleStatus = async (todo: Todo) => {
    try {
      const newStatus = todo.status === 'completed' ? 'pending' : 'completed';
      const updatedTodo = await apiService.updateTodo(todo.id, { status: newStatus });
      setTodos(todos.map(t => t.id === todo.id ? updatedTodo : t));
    } catch (error) {
      console.error('Error updating todo:', error);
    }
  };

  const handlePlanWithAI = async () => {
    if (todos.length === 0) return;

    try {
      setAiLoading(true);
      const tasks = todos.map(todo => todo.title);
      const plan = await apiService.planWithAI(tasks);
      setAiPlan(plan);
      setAiDialogOpen(true);
    } catch (error) {
      console.error('Error planning with AI:', error);
    } finally {
      setAiLoading(false);
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high': return 'error';
      case 'medium': return 'warning';
      case 'low': return 'success';
      default: return 'default';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed': return 'success';
      case 'in_progress': return 'warning';
      case 'pending': return 'default';
      default: return 'default';
    }
  };

  return (
    <Box sx={{ minHeight: '100vh', bgcolor: 'background.default' }}>
      {/* App Bar */}
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            AITodo
          </Typography>
          <IconButton
            color="inherit"
            onClick={(e) => setAnchorEl(e.currentTarget)}
          >
            <Avatar sx={{ width: 32, height: 32 }}>
              {user?.profile_picture ? (
                <img src={user.profile_picture} alt="Profile" />
              ) : (
                <PersonIcon />
              )}
            </Avatar>
          </IconButton>
          <Menu
            anchorEl={anchorEl}
            open={Boolean(anchorEl)}
            onClose={() => setAnchorEl(null)}
          >
            <MenuItem disabled>
              <Typography variant="body2">
                {user?.email}
              </Typography>
            </MenuItem>
            <MenuItem onClick={logout}>
              <LogoutIcon sx={{ mr: 1 }} />
              Logout
            </MenuItem>
          </Menu>
        </Toolbar>
      </AppBar>

      <Container maxWidth="md" sx={{ py: 4 }}>
        {/* Input Section */}
        <Box sx={{ mb: 4 }}>
          <Typography variant="h4" gutterBottom>
            Add New Task
          </Typography>
          <Box sx={{ display: 'flex', gap: 2, mb: 2 }}>
            <TextField
              fullWidth
              variant="outlined"
              placeholder="Enter your task..."
              value={newTodo}
              onChange={(e) => setNewTodo(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleAddTodo()}
            />
            <Button
              variant="contained"
              onClick={handleAddTodo}
              disabled={!newTodo.trim()}
              startIcon={<AddIcon />}
            >
              Add
            </Button>
            <Button
              variant="outlined"
              onClick={handlePlanWithAI}
              disabled={todos.length === 0 || aiLoading}
              startIcon={aiLoading ? <CircularProgress size={20} /> : <AIIcon />}
            >
              Plan with AI
            </Button>
          </Box>
        </Box>

        {/* Todos List */}
        <Box>
          <Typography variant="h5" gutterBottom>
            Your Tasks ({todos.length})
          </Typography>
          
          {loading ? (
            <Box display="flex" justifyContent="center" py={4}>
              <CircularProgress />
            </Box>
          ) : todos.length === 0 ? (
            <Card>
              <CardContent sx={{ textAlign: 'center', py: 4 }}>
                <Typography variant="h6" color="text.secondary">
                  No tasks yet. Add your first task above!
                </Typography>
              </CardContent>
            </Card>
          ) : (
            <List>
              {todos.map((todo) => (
                <Card key={todo.id} sx={{ mb: 2 }}>
                  <CardContent>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                      <IconButton
                        onClick={() => handleToggleStatus(todo)}
                        color={todo.status === 'completed' ? 'success' : 'default'}
                      >
                        <CheckIcon />
                      </IconButton>
                      
                      <Box sx={{ flexGrow: 1 }}>
                        <Typography
                          variant="h6"
                          sx={{
                            textDecoration: todo.status === 'completed' ? 'line-through' : 'none',
                            color: todo.status === 'completed' ? 'text.secondary' : 'text.primary',
                          }}
                        >
                          {todo.title}
                        </Typography>
                        {todo.description && (
                          <Typography variant="body2" color="text.secondary">
                            {todo.description}
                          </Typography>
                        )}
                        <Box sx={{ mt: 1, display: 'flex', gap: 1 }}>
                          <Chip
                            label={todo.priority}
                            size="small"
                            color={getPriorityColor(todo.priority) as any}
                          />
                          <Chip
                            label={todo.status.replace('_', ' ')}
                            size="small"
                            color={getStatusColor(todo.status) as any}
                          />
                        </Box>
                      </Box>
                      
                      <IconButton
                        color="error"
                        onClick={() => handleDeleteTodo(todo.id)}
                      >
                        <DeleteIcon />
                      </IconButton>
                    </Box>
                  </CardContent>
                </Card>
              ))}
            </List>
          )}
        </Box>
      </Container>

      {/* AI Planning Dialog */}
      <Dialog
        open={aiDialogOpen}
        onClose={() => setAiDialogOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          <Box display="flex" alignItems="center" gap={1}>
            <AIIcon color="primary" />
            AI Planning Results
          </Box>
        </DialogTitle>
        <DialogContent>
          {aiPlan && (
            <Box>
              <Typography variant="h6" gutterBottom>
                Planning Strategy
              </Typography>
              <Typography variant="body1" paragraph sx={{ whiteSpace: 'pre-line' }}>
                {aiPlan.plan}
              </Typography>
              
              <Typography variant="h6" gutterBottom sx={{ mt: 3 }}>
                Prioritized Tasks
              </Typography>
              <List>
                {aiPlan.prioritized_tasks.map((task, index) => (
                  <ListItem key={index}>
                    <ListItemText
                      primary={task.task}
                      secondary={`${task.estimated_time} • Priority: ${task.priority}`}
                    />
                    <Chip
                      label={`#${task.order}`}
                      size="small"
                      color={getPriorityColor(task.priority) as any}
                    />
                  </ListItem>
                ))}
              </List>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setAiDialogOpen(false)}>
            Close
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default TodoApp; 