'use client';

import React from 'react';
import { Box, CircularProgress, Typography } from '@mui/material';

interface LoadingSpinnerProps {
  message?: string;
  size?: number;
  fullScreen?: boolean;
}

export const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  message = 'Loading...',
  size = 40,
  fullScreen = false,
}) => {
  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        gap: 2,
        height: fullScreen ? '100vh' : 'auto',
        width: fullScreen ? '100vw' : 'auto',
        position: fullScreen ? 'fixed' : 'relative',
        top: 0,
        left: 0,
        bgcolor: fullScreen ? 'background.paper' : 'transparent',
        zIndex: fullScreen ? 9999 : 'auto',
      }}
    >
      <CircularProgress size={size} />
      {message && (
        <Typography variant="body1" color="text.secondary">
          {message}
        </Typography>
      )}
    </Box>
  );
};

export default LoadingSpinner;