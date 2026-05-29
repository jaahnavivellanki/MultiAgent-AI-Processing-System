import React, { useState } from 'react';
import {
  Container,
  Paper,
  Typography,
  Box,
  Button,
  TextField,
  CircularProgress,
  Alert,
  Tabs,
  Tab,
  Card,
  CardContent,
  ThemeProvider,
  createTheme,
  CssBaseline,
  AppBar,
  Toolbar,
  IconButton,
} from '@mui/material';
import { Upload as UploadIcon, Send as SendIcon, Brightness4 as DarkModeIcon } from '@mui/icons-material';
import axios from 'axios';

const API_URL = 'http://localhost:8000';

// Create a custom theme
const theme = createTheme({
  palette: {
    primary: {
      main: '#2196f3',
    },
    secondary: {
      main: '#f50057',
    },
    background: {
      default: '#f5f5f5',
      paper: '#ffffff',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h4: {
      fontWeight: 600,
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          textTransform: 'none',
          padding: '8px 24px',
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
        },
      },
    },
  },
});

function App() {
  const [file, setFile] = useState(null);
  const [text, setText] = useState('');
  const [jsonData, setJsonData] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);
  const [activeTab, setActiveTab] = useState(0);
  const [darkMode, setDarkMode] = useState(false);

  const handleFileChange = (event) => {
    setFile(event.target.files[0]);
  };

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
    setFile(null);
    setText('');
    setJsonData('');
    setResult(null);
    setError(null);
  };

  const handleSubmit = async () => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const formData = new FormData();
      
      if (file) {
        formData.append('file', file);
      } else if (text) {
        formData.append('text', text);
      } else if (jsonData) {
        formData.append('json_data', jsonData);
      }

      const response = await axios.post(`${API_URL}/process`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.detail || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ flexGrow: 1, minHeight: '100vh', bgcolor: 'background.default' }}>
        <AppBar position="static" elevation={0}>
          <Toolbar>
            <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
              AI Processing System
            </Typography>
            <IconButton color="inherit" onClick={() => setDarkMode(!darkMode)}>
              <DarkModeIcon />
            </IconButton>
          </Toolbar>
        </AppBar>

        <Container maxWidth="md" sx={{ py: 4 }}>
          <Paper 
            elevation={3} 
            sx={{ 
              p: 4, 
              borderRadius: 2,
              bgcolor: 'background.paper',
              boxShadow: '0 8px 16px rgba(0, 0, 0, 0.1)'
            }}
          >
            <Typography 
              variant="h4" 
              component="h1" 
              gutterBottom 
              align="center"
              sx={{ 
                mb: 4,
                color: 'primary.main',
                fontWeight: 'bold'
              }}
            >
              Multi-Format AI Processing System
            </Typography>

            <Tabs 
              value={activeTab} 
              onChange={handleTabChange} 
              centered 
              sx={{ 
                mb: 4,
                '& .MuiTab-root': {
                  fontSize: '1rem',
                  fontWeight: 500,
                }
              }}
            >
              <Tab label="File Upload" />
              <Tab label="Text Input" />
              <Tab label="JSON Input" />
            </Tabs>

            <Box sx={{ mb: 4 }}>
              {activeTab === 0 && (
                <Box 
                  sx={{ 
                    textAlign: 'center',
                    p: 3,
                    border: '2px dashed',
                    borderColor: 'primary.main',
                    borderRadius: 2,
                    bgcolor: 'background.default'
                  }}
                >
                  <input
                    accept=".pdf,.txt,.eml"
                    style={{ display: 'none' }}
                    id="file-upload"
                    type="file"
                    onChange={handleFileChange}
                  />
                  <label htmlFor="file-upload">
                    <Button
                      variant="contained"
                      component="span"
                      startIcon={<UploadIcon />}
                      size="large"
                    >
                      Choose File
                    </Button>
                  </label>
                  {file && (
                    <Typography 
                      variant="body1" 
                      sx={{ 
                        mt: 2,
                        color: 'primary.main',
                        fontWeight: 500
                      }}
                    >
                      Selected: {file.name}
                    </Typography>
                  )}
                </Box>
              )}

              {activeTab === 1 && (
                <TextField
                  fullWidth
                  multiline
                  rows={6}
                  variant="outlined"
                  label="Enter Text"
                  value={text}
                  onChange={(e) => setText(e.target.value)}
                  sx={{
                    '& .MuiOutlinedInput-root': {
                      borderRadius: 2,
                    }
                  }}
                />
              )}

              {activeTab === 2 && (
                <TextField
                  fullWidth
                  multiline
                  rows={6}
                  variant="outlined"
                  label="Enter JSON"
                  value={jsonData}
                  onChange={(e) => setJsonData(e.target.value)}
                  sx={{
                    '& .MuiOutlinedInput-root': {
                      borderRadius: 2,
                    }
                  }}
                />
              )}
            </Box>

            <Box sx={{ textAlign: 'center', mb: 4 }}>
              <Button
                variant="contained"
                color="primary"
                onClick={handleSubmit}
                disabled={loading || (!file && !text && !jsonData)}
                startIcon={loading ? <CircularProgress size={20} /> : <SendIcon />}
                size="large"
                sx={{
                  minWidth: 200,
                  height: 48,
                }}
              >
                {loading ? 'Processing...' : 'Process'}
              </Button>
            </Box>

            {error && (
              <Alert 
                severity="error" 
                sx={{ 
                  mb: 3,
                  borderRadius: 2,
                }}
              >
                {error}
              </Alert>
            )}

            {result && (
              <Box>
                <Typography 
                  variant="h5" 
                  gutterBottom
                  sx={{ 
                    color: 'primary.main',
                    fontWeight: 'bold',
                    mb: 3
                  }}
                >
                  Results
                </Typography>
                
                <Card sx={{ mb: 3 }}>
                  <CardContent>
                    <Typography 
                      variant="h6" 
                      gutterBottom
                      sx={{ color: 'primary.main' }}
                    >
                      Classification
                    </Typography>
                    <Box 
                      sx={{ 
                        p: 2, 
                        bgcolor: 'background.default',
                        borderRadius: 1,
                        overflow: 'auto'
                      }}
                    >
                      <Typography variant="body2" component="pre">
                        {JSON.stringify(result.classification, null, 2)}
                      </Typography>
                    </Box>
                  </CardContent>
                </Card>

                <Card sx={{ mb: 3 }}>
                  <CardContent>
                    <Typography 
                      variant="h6" 
                      gutterBottom
                      sx={{ color: 'primary.main' }}
                    >
                      Processed Data
                    </Typography>
                    {result.processed_data && result.processed_data.type === 'email' && (
                      <>
                        {result.processed_data.metadata && (
                          <Box sx={{ mb: 2 }}>
                            <p><strong>Sender:</strong> {result.processed_data.metadata.sender}</p>
                            <p><strong>Subject:</strong> {result.processed_data.metadata.subject}</p>
                            <p><strong>Date:</strong> {result.processed_data.metadata.date}</p>
                          </Box>
                        )}
                        {result.processed_data.content && (
                           <Box 
                             sx={{ 
                               p: 2, 
                               bgcolor: 'background.default',
                               borderRadius: 1,
                               overflow: 'auto',
                               whiteSpace: 'pre-wrap',
                               mt: 2 // Add some margin top to separate from metadata
                             }}
                           >
                             <Typography variant="body2">
                               {result.processed_data.content}
                             </Typography>
                           </Box>
                        )}
                      </>
                    )}
                    {result.processed_data && result.processed_data.type === 'json' && (
                      <Box 
                        sx={{ 
                          p: 2, 
                          bgcolor: 'background.default',
                          borderRadius: 1,
                          overflow: 'auto',
                          whiteSpace: 'pre-wrap'
                        }}
                      >
                        <Typography variant="body2" component="pre">
                          {JSON.stringify(result.processed_data.data, null, 2)}
                        </Typography>
                      </Box>
                    )}
                     {result.processed_data && result.processed_data.type === 'pdf' && (
                       <Box 
                         sx={{ 
                           p: 2, 
                           bgcolor: 'background.default',
                           borderRadius: 1,
                           overflow: 'auto',
                           whiteSpace: 'pre-wrap',
                           mt: 2 // Add some margin top to separate from metadata
                         }}
                       >
                         <Typography variant="body2">
                           {result.processed_data.content}
                         </Typography>
                          {result.processed_data.metadata && (
                            <Box sx={{ mt: 2 }}>
                              <Typography variant="body2"><strong>Title:</strong> {result.processed_data.metadata.title}</Typography>
                              <Typography variant="body2"><strong>Author:</strong> {result.processed_data.metadata.author}</Typography>
                              <Typography variant="body2"><strong>Pages:</strong> {result.processed_data.metadata.pages}</Typography>
                              <Typography variant="body2"><strong>Creation Date:</strong> {result.processed_data.metadata.creation_date}</Typography>
                            </Box>
                          )}
                       </Box>
                    )}
                  </CardContent>
                </Card>

                <Card>
                  <CardContent>
                    <Typography 
                      variant="h6" 
                      gutterBottom
                      sx={{ color: 'primary.main' }}
                    >
                      Action
                    </Typography>
                    <Box 
                      sx={{ 
                        p: 2, 
                        bgcolor: 'background.default',
                        borderRadius: 1,
                        overflow: 'auto'
                      }}
                    >
                      <Typography variant="body2" component="pre">
                        {JSON.stringify(result.action, null, 2)}
                      </Typography>
                    </Box>
                  </CardContent>
                </Card>
              </Box>
            )}
          </Paper>
        </Container>
      </Box>
    </ThemeProvider>
  );
}

export default App; 