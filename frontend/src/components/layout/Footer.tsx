'use client';

import React from 'react';
import { Box, Container, Typography, Link as MuiLink } from '@mui/material';
import Link from 'next/link';

const Footer: React.FC = () => {
  return (
    <Box
      component="footer"
      sx={{
        py: 3,
        px: 2,
        mt: 'auto',
        backgroundColor: 'background.paper',
        borderTop: 1,
        borderColor: 'divider',
      }}
    >
      <Container maxWidth="lg">
        <Box
          sx={{
            display: 'flex',
            flexDirection: { xs: 'column', sm: 'row' },
            justifyContent: 'space-between',
            alignItems: 'center',
            gap: 2,
          }}
        >
          <Typography variant="body2" color="text.secondary">
            © {new Date().getFullYear()} CV Villas Knowledge Assistant. All rights reserved.
          </Typography>
          
          <Box sx={{ display: 'flex', gap: 3 }}>
            <MuiLink
              component={Link}
              href="/privacy"
              variant="body2"
              color="text.secondary"
              sx={{ textDecoration: 'none', '&:hover': { textDecoration: 'underline' } }}
            >
              Privacy Policy
            </MuiLink>
            <MuiLink
              component={Link}
              href="/terms"
              variant="body2"
              color="text.secondary"
              sx={{ textDecoration: 'none', '&:hover': { textDecoration: 'underline' } }}
            >
              Terms of Service
            </MuiLink>
            <MuiLink
              component={Link}
              href="/support"
              variant="body2"
              color="text.secondary"
              sx={{ textDecoration: 'none', '&:hover': { textDecoration: 'underline' } }}
            >
              Support
            </MuiLink>
          </Box>
        </Box>
        
        <Typography variant="caption" color="text.secondary" sx={{ display: 'block', mt: 2, textAlign: 'center' }}>
          Version 1.0 • Powered by Next.js 14 & Material-UI
        </Typography>
      </Container>
    </Box>
  );
};

export default Footer;