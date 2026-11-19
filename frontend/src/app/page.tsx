import { Box, Button, Container, Grid, Typography, Paper, Stack } from '@mui/material';
import { Villa, QuestionAnswer, History, VerifiedUser, Dashboard, AdminPanelSettings } from '@mui/icons-material';
import Link from 'next/link';

export default function HomePage() {
  return (
    <Box sx={{ bgcolor: 'background.default', minHeight: '100vh' }}>
      {/* Hero Section */}
      <Box
        sx={{
          background: 'linear-gradient(135deg, #2c3e50 0%, #1976d2 100%)',
          color: 'white',
          py: 10,
          px: 2,
          textAlign: 'center',
        }}
      >
        <Container maxWidth="lg">
          <Villa sx={{ fontSize: 80, mb: 3 }} />
          <Typography variant="h2" component="h1" gutterBottom sx={{ fontWeight: 700 }}>
            CV Villas Agent Assist
          </Typography>
          <Typography variant="h5" component="h2" sx={{ mb: 4, opacity: 0.9, maxWidth: 800, mx: 'auto' }}>
            Your AI-powered knowledge assistant for villa rental sales. Get instant answers with citations, 
            expert corrections, and comprehensive coverage insights.
          </Typography>
          <Stack direction="row" spacing={2} justifyContent="center" sx={{ mt: 4 }}>
            <Button
              component={Link}
              href="/login"
              variant="contained"
              size="large"
              sx={{
                bgcolor: 'white',
                color: '#1976d2',
                '&:hover': { bgcolor: '#f5f5f5' },
                px: 4,
                py: 1.5,
              }}
            >
              Get Started
            </Button>
            <Button
              component={Link}
              href="/dashboard"
              variant="outlined"
              size="large"
              sx={{
                borderColor: 'white',
                color: 'white',
                '&:hover': { borderColor: '#f5f5f5', color: '#f5f5f5' },
                px: 4,
                py: 1.5,
              }}
            >
              Demo Dashboard
            </Button>
          </Stack>
        </Container>
      </Box>

      {/* Features Section */}
      <Container maxWidth="lg" sx={{ py: 8, px: 2 }}>
        <Typography variant="h3" component="h2" gutterBottom sx={{ textAlign: 'center', mb: 6 }}>
          Key Features
        </Typography>
        <Grid container spacing={4}>
          <Grid item xs={12} md={4}>
            <Paper
              elevation={2}
              sx={{
                p: 3,
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                textAlign: 'center',
                transition: 'transform 0.2s',
                '&:hover': { transform: 'translateY(-4px)' },
              }}
            >
              <QuestionAnswer sx={{ fontSize: 60, color: 'primary.main', mb: 2 }} />
              <Typography variant="h5" component="h3" gutterBottom>
                Instant Q&A
              </Typography>
              <Typography color="text.secondary">
                Ask villa-related questions and receive accurate, citation-backed answers instantly. 
                Perfect for sales situations requiring quick, reliable information.
              </Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} md={4}>
            <Paper
              elevation={2}
              sx={{
                p: 3,
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                textAlign: 'center',
                transition: 'transform 0.2s',
                '&:hover': { transform: 'translateY(-4px)' },
              }}
            >
              <History sx={{ fontSize: 60, color: 'secondary.main', mb: 2 }} />
              <Typography variant="h5" component="h3" gutterBottom>
                Answer History
              </Typography>
              <Typography color="text.secondary">
                Track all your previous questions and answers. Review conversations, 
                citations, and confidence scores to improve your knowledge base over time.
              </Typography>
            </Paper>
          </Grid>
          <Grid item xs={12} md={4}>
            <Paper
              elevation={2}
              sx={{
                p: 3,
                height: '100%',
                display: 'flex',
                flexDirection: 'column',
                alignItems: 'center',
                textAlign: 'center',
                transition: 'transform 0.2s',
                '&:hover': { transform: 'translateY(-4px)' },
              }}
            >
              <VerifiedUser sx={{ fontSize: 60, color: 'success.main', mb: 2 }} />
              <Typography variant="h5" component="h3" gutterBottom>
                Expert Verifications
              </Typography>
              <Typography color="text.secondary">
                Domain experts can review and correct answers, ensuring information 
                accuracy. Corrections are tracked and audited for quality assurance.
              </Typography>
            </Paper>
          </Grid>
        </Grid>

        {/* Role-Based Sections */}
        <Box sx={{ mt: 10 }}>
          <Typography variant="h4" component="h2" gutterBottom sx={{ textAlign: 'center', mb: 6 }}>
            Role-Specific Experiences
          </Typography>
          <Grid container spacing={4}>
            <Grid item xs={12} md={6}>
              <Paper
                elevation={1}
                sx={{
                  p: 4,
                  borderLeft: 4,
                  borderColor: 'primary.main',
                  height: '100%',
                }}
              >
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Dashboard sx={{ mr: 2, color: 'primary.main' }} />
                  <Typography variant="h5" component="h3">
                    For Sales Agents
                  </Typography>
                </Box>
                <Typography color="text.secondary" paragraph>
                  Access the full knowledge base to answer customer questions about villa amenities, 
                  policies, pricing, and availability. Get confidence scores and citations for every answer.
                </Typography>
                <ul style={{ marginLeft: '1.5rem', color: 'text.secondary' }}>
                  <li>Ask questions in natural language</li>
                  <li>View answer confidence scores</li>
                  <li>Access citation sources</li>
                  <li>Track question history</li>
                </ul>
              </Paper>
            </Grid>
            <Grid item xs={12} md={6}>
              <Paper
                elevation={1}
                sx={{
                  p: 4,
                  borderLeft: 4,
                  borderColor: 'secondary.main',
                  height: '100%',
                }}
              >
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <AdminPanelSettings sx={{ mr: 2, color: 'secondary.main' }} />
                  <Typography variant="h5" component="h3">
                    For Experts & Admins
                  </Typography>
                </Box>
                <Typography color="text.secondary" paragraph>
                  Review and correct answers, manage knowledge sources, track coverage gaps, 
                  and oversee system health. Ensure information accuracy and quality.
                </Typography>
                <ul style={{ marginLeft: '1.5rem', color: 'text.secondary' }}>
                  <li>Submit expert corrections</li>
                  <li>Review coverage gaps</li>
                  <li>Manage knowledge sources</li>
                  <li>Monitor audit logs</li>
                </ul>
              </Paper>
            </Grid>
          </Grid>
        </Box>

        {/* CTA Section */}
        <Box sx={{ textAlign: 'center', mt: 10, p: 4, bgcolor: 'background.paper', borderRadius: 2 }}>
          <Typography variant="h4" component="h2" gutterBottom>
            Ready to Transform Your Sales Support?
          </Typography>
          <Typography variant="body1" color="text.secondary" sx={{ mb: 4, maxWidth: 600, mx: 'auto' }}>
            Join agents who are already using CV Villas Agent Assist to provide better, 
            faster customer service with confidence.
          </Typography>
          <Button
            component={Link}
            href="/login"
            variant="contained"
            size="large"
            sx={{ px: 6, py: 1.5 }}
          >
            Start Your Free Trial
          </Button>
        </Box>
      </Container>
    </Box>
  );
}