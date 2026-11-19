'use client';

// Placeholder stub for 23aaade8-d107-4d70-8d0a-d275d3e80c7b_TASK-03 - Agent Dashboard & Core Q&A Interactive Experience
// This is a minimal placeholder page that will be fully implemented in Wave 2.

import { Box, Container, Typography, Button, Paper } from '@mui/material';
import { ArrowForward, QuestionAnswer } from '@mui/icons-material';
import Link from 'next/link';

export default function DashboardPlaceholder() {
  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Paper elevation={2} sx={{ p: 6, borderRadius: 2, textAlign: 'center' }}>
        <Box mb={4}>
          <QuestionAnswer sx={{ fontSize: 64, color: 'primary.main', mb: 2 }} />
          <Typography variant="h4" component="h1" gutterBottom sx={{ fontWeight: 600 }}>
            Dashboard (Coming Soon)
          </Typography>
          <Typography variant="body1" color="text.secondary" paragraph sx={{ maxWidth: 600, mx: 'auto', mb: 4 }}>
            The Agent Dashboard with intelligent Q&A, answer history, and citation display will be available in the next release.
            This is where agents will ask questions and receive AI-powered answers with source citations.
          </Typography>
        </Box>
        
        <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 2 }}>
          <Typography variant="body2" color="text.secondary">
            In the meantime, you can:
          </Typography>
          <Button
            component={Link}
            href="/"
            variant="outlined"
            size="medium"
            sx={{ px: 4 }}
          >
            Return to Home
          </Button>
        </Box>
      </Paper>
    </Container>
  );
}