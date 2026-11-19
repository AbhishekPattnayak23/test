'use client';

import { CircularProgress, Box } from '@mui/material';

interface LoadingSpinnerProps {
  size?: number;
  centered?: boolean;
  label?: string;
}

export default function LoadingSpinner({ 
  size = 40, 
  centered = true, 
  label 
}: LoadingSpinnerProps) {
  const spinner = (
    <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
      <CircularProgress size={size} />
      {label && <span>{label}</span>}
    </Box>
  );

  if (centered) {
    return (
      <Box 
        sx={{ 
          display: 'flex', 
          justifyContent: 'center', 
          alignItems: 'center', 
          minHeight: 200 
        }}
      >
        {spinner}
      </Box>
    );
  }

  return spinner;
}
