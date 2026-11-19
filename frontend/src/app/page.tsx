import { Button, Card, CardContent, Container, Grid, Typography, Box, Stack, Paper } from '@mui/material'
import { ArrowForward, QuestionAnswer, History, AdminPanelSettings, AutoStories, GppGood } from '@mui/icons-material'
import Link from 'next/link'

export default function HomePage() {
  return (
    <Container maxWidth="lg" sx={{ py: 6 }}>
      {/* Hero Section */}
      <Box textAlign="center" mb={8}>
        <Typography variant="h2" component="h1" gutterBottom sx={{ fontWeight: 700, color: 'primary.main' }}>
          Villa Knowledge Assistant
        </Typography>
        <Typography variant="h5" color="text.secondary" paragraph sx={{ maxWidth: 800, mx: 'auto' }}>
          AI-powered knowledge assistant empowering villa rental sales agents with instant, accurate answers and comprehensive support resources.
        </Typography>
        <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2} justifyContent="center" mt={4}>
          <Button
            component={Link}
            href="/dashboard"
            variant="contained"
            size="large"
            endIcon={<ArrowForward />}
            sx={{ px: 4 }}
          >
            Go to Dashboard
          </Button>
          <Button
            component={Link}
            href="/login"
            variant="outlined"
            size="large"
            sx={{ px: 4 }}
          >
            Sign In
          </Button>
        </Stack>
      </Box>

      {/* Features Grid */}
      <Typography variant="h4" component="h2" gutterBottom textAlign="center" mb={4}>
        Key Features
      </Typography>
      <Grid container spacing={4} mb={8}>
        {[
          {
            icon: <QuestionAnswer sx={{ fontSize: 40, color: 'primary.main' }} />,
            title: 'Intelligent Q&A',
            description: 'Ask natural language questions about villa policies, amenities, and reservations. Get instant answers with source citations.',
          },
          {
            icon: <History sx={{ fontSize: 40, color: 'primary.main' }} />,
            title: 'Answer History',
            description: 'Track all previous questions and answers. Quickly reference past conversations with clients.',
          },
          {
            icon: <AutoStories sx={{ fontSize: 40, color: 'primary.main' }} />,
            title: 'Knowledge Base',
            description: 'Access comprehensive villa documentation, FAQs, and expert knowledge curated from multiple sources.',
          },
          {
            icon: <GppGood sx={{ fontSize: 40, color: 'primary.main' }} />,
            title: 'Expert Corrections',
            description: 'Submit corrections for inaccurate answers. Continuous improvement through expert feedback.',
          },
          {
            icon: <AdminPanelSettings sx={{ fontSize: 40, color: 'primary.main' }} />,
            title: 'Admin Dashboard',
            description: 'Manage users, audit logs, knowledge sources, and monitor system performance (admin roles only).',
          },
        ].map((feature, index) => (
          <Grid item xs={12} sm={6} md={4} key={index}>
            <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
              <CardContent sx={{ flexGrow: 1, textAlign: 'center' }}>
                <Box mb={2}>{feature.icon}</Box>
                <Typography variant="h6" gutterBottom>
                  {feature.title}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {feature.description}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* How It Works */}
      <Paper elevation={2} sx={{ p: 4, mb: 8, borderRadius: 2 }}>
        <Typography variant="h4" component="h2" gutterBottom textAlign="center">
          How It Works
        </Typography>
        <Grid container spacing={4} mt={2}>
          {[
            { step: '1', title: 'Ask Questions', description: 'Sales agents submit questions about villa rentals in natural language.' },
            { step: '2', title: 'Get AI-Powered Answers', description: 'Our assistant analyzes knowledge sources and provides accurate answers with confidence scores.' },
            { step: '3', title: 'View Citations', description: 'Every answer includes source citations so you can verify information.' },
            { step: '4', title: 'Continuous Improvement', description: 'Experts can submit corrections to improve the knowledge base over time.' },
          ].map((item) => (
            <Grid item xs={12} md={3} key={item.step}>
              <Box textAlign="center">
                <Box
                  sx={{
                    width: 60,
                    height: 60,
                    borderRadius: '50%',
                    bgcolor: 'primary.main',
                    color: 'white',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    fontSize: 24,
                    fontWeight: 'bold',
                    mx: 'auto',
                    mb: 2,
                  }}
                >
                  {item.step}
                </Box>
                <Typography variant="h6" gutterBottom>
                  {item.title}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {item.description}
                </Typography>
              </Box>
            </Grid>
          ))}
        </Grid>
      </Paper>

      {/* User Roles */}
      <Box mb={8}>
        <Typography variant="h4" component="h2" gutterBottom textAlign="center">
          Designed for Every Role
        </Typography>
        <Grid container spacing={4} mt={2}>
          {[
            {
              role: 'Sales Agent',
              description: 'Quick access to villa information, cancellation policies, amenities, and client-specific answers.',
              color: 'primary.light',
            },
            {
              role: 'Expert',
              description: 'Review and correct answers, contribute expert knowledge, and maintain content accuracy.',
              color: 'secondary.light',
            },
            {
              role: 'Admin',
              description: 'Manage users, monitor system usage, audit activities, and configure knowledge sources.',
              color: 'success.light',
            },
          ].map((userRole, index) => (
            <Grid item xs={12} md={4} key={index}>
              <Card sx={{ bgcolor: userRole.color, p: 3, height: '100%' }}>
                <Typography variant="h5" gutterBottom>
                  {userRole.role}
                </Typography>
                <Typography variant="body2">
                  {userRole.description}
                </Typography>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>

      {/* Call to Action */}
      <Box textAlign="center" sx={{ py: 6, bgcolor: 'background.paper', borderRadius: 2 }}>
        <Typography variant="h5" gutterBottom>
          Ready to enhance your villa rental support?
        </Typography>
        <Typography variant="body1" color="text.secondary" paragraph sx={{ maxWidth: 600, mx: 'auto', mb: 4 }}>
          Join our knowledge assistant platform and provide exceptional service to your clients with accurate, instant information.
        </Typography>
        <Button
          component={Link}
          href="/dashboard"
          variant="contained"
          size="large"
          endIcon={<ArrowForward />}
          sx={{ px: 6 }}
        >
          Get Started Now
        </Button>
      </Box>
    </Container>
  )
}