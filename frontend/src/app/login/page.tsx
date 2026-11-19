'use client';

import { useState } from 'react';
import {
  Box,
  Button,
  Card,
  CardContent,
  Container,
  TextField,
  Typography,
  Alert,
  CircularProgress,
  Divider,
} from '@mui/material';
import { Login as LoginIcon, LockOpen, Visibility, VisibilityOff } from '@mui/icons-material';
import Link from 'next/link';
import { useAuth } from '@/lib/auth/auth';

export default function LoginPage() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const { login, error, loading } = useAuth();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    try {
      await login(email, password);
    } catch (err) {
      // Error is handled by auth context
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleClickShowPassword = () => {
    setShowPassword(!showPassword);
  };

  return (
    <Container maxWidth="sm" sx={{ py: 8 }}>
      <Card elevation={3} sx={{ borderRadius: 3 }}>
        <CardContent sx={{ p: 4 }}>
          <Box textAlign="center" mb={4}>
            <LockOpen sx={{ fontSize: 64, color: 'primary.main', mb: 2 }} />
            <Typography variant="h4" component="h1" gutterBottom fontWeight={600}>
              Sign In
            </Typography>
            <Typography variant="body1" color="text.secondary">
              Access your villa knowledge assistant account
            </Typography>
          </Box>

          {error && (
            <Alert severity="error" sx={{ mb: 3 }}>
              {error}
            </Alert>
          )}

          <form onSubmit={handleSubmit}>
            <Box mb={3}>
              <TextField
                fullWidth
                label="Email Address"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                disabled={loading || isSubmitting}
                InputProps={{
                  endAdornment: <LoginIcon sx={{ color: 'action.disabled', ml: 1 }} />,
                }}
              />
            </Box>

            <Box mb={3}>
              <TextField
                fullWidth
                label="Password"
                type={showPassword ? 'text' : 'password'}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                disabled={loading || isSubmitting}
                InputProps={{
                  endAdornment: (
                    <Button
                      size="small"
                      onClick={handleClickShowPassword}
                      sx={{ minWidth: 'auto', pr: 1 }}
                    >
                      {showPassword ? <VisibilityOff /> : <Visibility />}
                    </Button>
                  ),
                }}
              />
            </Box>

            <Button
              fullWidth
              type="submit"
              variant="contained"
              size="large"
              disabled={!email || !password || loading || isSubmitting}
              sx={{ py: 1.5, mb: 3 }}
            >
              {isSubmitting ? (
                <CircularProgress size={24} color="inherit" />
              ) : (
                <>
                  Sign In
                  <LoginIcon sx={{ ml: 1 }} />
                </>
              )}
            </Button>
          </form>

          <Divider sx={{ my: 3 }} />

          <Box textAlign="center">
            <Typography variant="body2" color="text.secondary" mb={2}>
              Demo credentials for testing:
            </Typography>
            <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1, mb: 3 }}>
              <Typography variant="caption" color="text.secondary">
                <strong>Agent:</strong> john.agent@cv-villas.com / password123
              </Typography>
              <Typography variant="caption" color="text.secondary">
                <strong>Expert:</strong> sarah.expert@cv-villas.com / password123
              </Typography>
              <Typography variant="caption" color="text.secondary">
                <strong>Admin:</strong> mike.admin@cv-villas.com / password123
              </Typography>
            </Box>

            <Typography variant="body2" color="text.secondary">
              Not a member yet?{' '}
              <Link href="/register" style={{ color: 'inherit', textDecoration: 'underline' }}>
                Request access
              </Link>
            </Typography>
            <Typography variant="body2" color="text.secondary" mt={1}>
              <Link href="/forgot-password" style={{ color: 'inherit' }}>
                Forgot your password?
              </Link>
            </Typography>
          </Box>
        </CardContent>
      </Card>

      <Box textAlign="center" mt={4}>
        <Typography variant="caption" color="text.secondary">
          Villa Knowledge Assistant v1.0 • Secure login via JWT authentication
        </Typography>
      </Box>
    </Container>
  );
}