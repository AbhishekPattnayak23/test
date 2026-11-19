'use client';

import { useState } from 'react';
import {
  Box,
  Button,
  Container,
  TextField,
  Typography,
  Paper,
  Alert,
  CircularProgress,
  InputAdornment,
  IconButton,
} from '@mui/material';
import { Visibility, VisibilityOff, Login as LoginIcon } from '@mui/icons-material';
import { useAuth } from '@/lib/auth/auth';
import { useRouter } from 'next/navigation';
import Link from 'next/link';
import { useSnackbar } from 'notistack';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const { login, isLoading } = useAuth();
  const router = useRouter();
  const { enqueueSnackbar } = useSnackbar();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (!email || !password) {
      setError('Please enter both email and password');
      return;
    }

    try {
      await login(email, password);
      enqueueSnackbar('Login successful!', { variant: 'success' });
      router.push('/dashboard');
    } catch (err: any) {
      setError(err.message || 'Invalid credentials');
      enqueueSnackbar('Login failed: ' + err.message, { variant: 'error' });
    }
  };

  const handleDemoLogin = async (role: 'agent' | 'expert' | 'admin') => {
    const demoCredentials = {
      agent: { email: 'agent@example.com', password: 'password' },
      expert: { email: 'expert@example.com', password: 'password' },
      admin: { email: 'admin@example.com', password: 'password' },
    };

    setEmail(demoCredentials[role].email);
    setPassword('password');
    
    try {
      await login(demoCredentials[role].email, 'password');
      enqueueSnackbar(`Logged in as ${role}`, { variant: 'success' });
      router.push('/dashboard');
    } catch (err: any) {
      setError('Demo login failed');
      enqueueSnackbar('Demo login failed', { variant: 'error' });
    }
  };

  return (
    <Box
      sx={{
        minHeight: '100vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        bgcolor: 'background.default',
        p: 2,
      }}
    >
      <Container maxWidth="sm">
        <Box sx={{ textAlign: 'center', mb: 4 }}>
          <Typography variant="h3" component="h1" gutterBottom sx={{ fontWeight: 600 }}>
            CV Villas Agent Assist
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Sign in to access your knowledge assistant
          </Typography>
        </Box>

        <Paper elevation={3} sx={{ p: 4 }}>
          <Typography variant="h5" component="h2" gutterBottom sx={{ fontWeight: 500 }}>
            Login
          </Typography>

          {error && (
            <Alert severity="error" sx={{ mb: 3 }}>
              {error}
            </Alert>
          )}

          <Box component="form" onSubmit={handleSubmit} sx={{ mt: 3 }}>
            <TextField
              fullWidth
              label="Email Address"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              disabled={isLoading}
              margin="normal"
              required
              autoComplete="email"
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <LoginIcon fontSize="small" color="action" />
                  </InputAdornment>
                ),
              }}
            />

            <TextField
              fullWidth
              label="Password"
              type={showPassword ? 'text' : 'password'}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              disabled={isLoading}
              margin="normal"
              required
              autoComplete="current-password"
              InputProps={{
                startAdornment: (
                  <InputAdornment position="start">
                    <LoginIcon fontSize="small" color="action" />
                  </InputAdornment>
                ),
                endAdornment: (
                  <InputAdornment position="end">
                    <IconButton
                      aria-label="toggle password visibility"
                      onClick={() => setShowPassword(!showPassword)}
                      edge="end"
                    >
                      {showPassword ? <VisibilityOff /> : <Visibility />}
                    </IconButton>
                  </InputAdornment>
                ),
              }}
            />

            <Button
              type="submit"
              fullWidth
              variant="contained"
              disabled={isLoading}
              size="large"
              sx={{ mt: 3, py: 1.5 }}
            >
              {isLoading ? (
                <CircularProgress size={24} color="inherit" />
              ) : (
                'Sign In'
              )}
            </Button>
          </Box>

          <Box sx={{ mt: 4, pt: 3, borderTop: 1, borderColor: 'divider' }}>
            <Typography variant="body2" color="text.secondary" gutterBottom sx={{ textAlign: 'center' }}>
              Quick demo logins:
            </Typography>
            <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
              <Button
                fullWidth
                variant="outlined"
                onClick={() => handleDemoLogin('agent')}
                disabled={isLoading}
                size="small"
              >
                Agent Demo
              </Button>
              <Button
                fullWidth
                variant="outlined"
                onClick={() => handleDemoLogin('expert')}
                disabled={isLoading}
                size="small"
              >
                Expert Demo
              </Button>
              <Button
                fullWidth
                variant="outlined"
                onClick={() => handleDemoLogin('admin')}
                disabled={isLoading}
                size="small"
              >
                Admin Demo
              </Button>
            </Box>
          </Box>

          <Box sx={{ mt: 4, textAlign: 'center' }}>
            <Typography variant="body2" color="text.secondary">
              Don't have an account?{' '}
              <Link href="/register" style={{ textDecoration: 'none', color: '#1976d2' }}>
                Request access
              </Link>
            </Typography>
          </Box>
        </Paper>

        <Box sx={{ mt: 4, textAlign: 'center' }}>
          <Typography variant="caption" color="text.secondary">
            © {new Date().getFullYear()} CV Villas Agent Assist. All rights reserved.
          </Typography>
        </Box>
      </Container>
    </Box>
  );
}