'use client';

// Placeholder stub for 23aaade8-d107-4d70-8d0a-d275d3e80c7b_TASK-03 - Agent Dashboard & Core Q&A Interactive Experience
// This is a minimal placeholder sidebar that will be fully implemented in Wave 2.

import React from 'react';
import { Box, Divider } from '@mui/material';
import { useAuth } from '@/lib/auth/auth';

const Sidebar: React.FC = () => {
  const { user } = useAuth();

  return (
    <Box
      sx={{
        width: { md: 240 },
        flexShrink: 0,
        borderRight: 1,
        borderColor: 'divider',
        display: { xs: 'none', md: 'block' },
        bgcolor: 'background.paper',
      }}
    >
      <Box sx={{ p: 2 }}>
        <Box sx={{ mb: 2 }}>
          <Divider sx={{ mb: 2 }} />
          <Box fontSize="caption.fontSize" color="text.secondary">
            Navigation placeholder for Wave 1.
          </Box>
          <Box fontSize="caption.fontSize" color="text.secondary" mt={1}>
            Full sidebar with role-based links will be implemented in Wave 2.
          </Box>
        </Box>
      </Box>
    </Box>
  );
};

export default Sidebar;