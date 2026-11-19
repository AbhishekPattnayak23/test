import { createTheme } from '@mui/material/styles';

declare module '@mui/material/styles' {
  interface Palette {
    neutral: {
      50: string;
      100: string;
      200: string;
      300: string;
      400: string;
      500: string;
      600: string;
      700: string;
      800: string;
      900: string;
    };
  }
  interface PaletteOptions {
    neutral?: {
      50: string;
      100: string;
      200: string;
      300: string;
      400: string;
      500: string;
      600: string;
      700: string;
      800: string;
      900: string;
    };
  }
}

const theme = createTheme({
  palette: {
    primary: {
      50: '#e6f0ff',
      100: '#cce0ff',
      200: '#99c2ff',
      300: '#66a3ff',
      400: '#3385ff',
      500: '#0066CC', // Primary Blue
      600: '#0052a3',
      700: '#003d7a',
      800: '#002952',
      900: '#001429',
      main: '#0066CC',
      light: '#3385ff',
      dark: '#0052a3',
      contrastText: '#ffffff',
    },
    secondary: {
      50: '#e6f6f4',
      100: '#cceed8',
      200: '#99ddd2',
      300: '#66ccc5',
      400: '#33bbb9',
      500: '#00a896', // Secondary Teal
      600: '#008678',
      700: '#00645a',
      800: '#00423c',
      900: '#00211e',
      main: '#00a896',
      light: '#33bbb9',
      dark: '#008678',
      contrastText: '#ffffff',
    },
    neutral: {
      50: '#f8f9fa',
      100: '#f1f3f5',
      200: '#e9ecef',
      300: '#dee2e6',
      400: '#ced4da',
      500: '#adb5bd',
      600: '#6c757d',
      700: '#495057',
      800: '#343a40',
      900: '#212529',
    },
    error: {
      main: '#dc3545',
      light: '#e57373',
      dark: '#d32f2f',
      contrastText: '#ffffff',
    },
    warning: {
      main: '#ffc107',
      light: '#ffd54f',
      dark: '#ff9800',
      contrastText: '#212529',
    },
    info: {
      main: '#17a2b8',
      light: '#4dd0e1',
      dark: '#0097a7',
      contrastText: '#ffffff',
    },
    success: {
      main: '#28a745',
      light: '#81c784',
      dark: '#388e3c',
      contrastText: '#ffffff',
    },
    background: {
      default: '#ffffff',
      paper: '#f8f9fa',
    },
    text: {
      primary: '#212529',
      secondary: '#6c757d',
      disabled: '#adb5bd',
    },
    divider: '#e9ecef',
  },
  typography: {
    fontFamily: [
      'Roboto',
      '-apple-system',
      'BlinkMacSystemFont',
      '\'Segoe UI\'',
      '\'Helvetica Neue\'',
      'Arial',
      'sans-serif',
    ].join(','),
    h1: {
      fontFamily: [
        'Inter',
        '-apple-system',
        'BlinkMacSystemFont',
        '\'Segoe UI\'',
        '\'Helvetica Neue\'',
        'Arial',
        'sans-serif',
      ].join(','),
      fontSize: '2.5rem', // 40px
      fontWeight: 700,
      lineHeight: 1.2,
    },
    h2: {
      fontFamily: [
        'Inter',
        '-apple-system',
        'BlinkMacSystemFont',
        '\'Segoe UI\'',
        '\'Helvetica Neue\'',
        'Arial',
        'sans-serif',
      ].join(','),
      fontSize: '2rem', // 32px
      fontWeight: 600,
      lineHeight: 1.3,
    },
    h3: {
      fontFamily: [
        'Inter',
        '-apple-system',
        'BlinkMacSystemFont',
        '\'Segoe UI\'',
        '\'Helvetica Neue\'',
        'Arial',
        'sans-serif',
      ].join(','),
      fontSize: '1.75rem', // 28px
      fontWeight: 600,
      lineHeight: 1.4,
    },
    h4: {
      fontFamily: [
        'Inter',
        '-apple-system',
        'BlinkMacSystemFont',
        '\'Segoe UI\'',
        '\'Helvetica Neue\'',
        'Arial',
        'sans-serif',
      ].join(','),
      fontSize: '1.5rem', // 24px
      fontWeight: 600,
      lineHeight: 1.4,
    },
    h5: {
      fontFamily: [
        'Inter',
        '-apple-system',
        'BlinkMacSystemFont',
        '\'Segoe UI\'',
        '\'Helvetica Neue\'',
        'Arial',
        'sans-serif',
      ].join(','),
      fontSize: '1.25rem', // 20px
      fontWeight: 500,
      lineHeight: 1.5,
    },
    h6: {
      fontFamily: [
        'Inter',
        '-apple-system',
        'BlinkMacSystemFont',
        '\'Segoe UI\'',
        '\'Helvetica Neue\'',
        'Arial',
        'sans-serif',
      ].join(','),
      fontSize: '1rem', // 16px
      fontWeight: 500,
      lineHeight: 1.5,
    },
    body1: {
      fontSize: '1rem', // 16px
      lineHeight: 1.6,
    },
    body2: {
      fontSize: '0.875rem', // 14px
      lineHeight: 1.6,
    },
    button: {
      textTransform: 'none',
      fontWeight: 500,
    },
  },
  shape: {
    borderRadius: 8,
  },
  spacing: 8, // Base spacing unit (8px)
  shadows: [
    'none',
    '0 1px 2px rgba(0, 0, 0, 0.05)',
    '0 1px 3px rgba(0, 0, 0, 0.1)',
    '0 4px 6px rgba(0, 0, 0, 0.1)',
    '0 10px 15px rgba(0, 0, 0, 0.1)',
    '0 20px 25px rgba(0, 0, 0, 0.1)',
    '0 25px 50px rgba(0, 0, 0, 0.1)',
    '0 35px 60px rgba(0, 0, 0, 0.1)',
    '0 45px 70px rgba(0, 0, 0, 0.1)',
    '0 55px 80px rgba(0, 0, 0, 0.1)',
    '0 65px 90px rgba(0, 0, 0, 0.1)',
    '0 75px 100px rgba(0, 0, 0, 0.1)',
    '0 85px 110px rgba(0, 0, 0, 0.1)',
    '0 95px 120px rgba(0, 0, 0, 0.1)',
    '0 105px 130px rgba(0, 0, 0, 0.1)',
    '0 115px 140px rgba(0, 0, 0, 0.1)',
    '0 125px 150px rgba(0, 0, 0, 0.1)',
    '0 135px 160px rgba(0, 0, 0, 0.1)',
    '0 145px 170px rgba(0, 0, 0, 0.1)',
    '0 155px 180px rgba(0, 0, 0, 0.1)',
    '0 165px 190px rgba(0, 0, 0, 0.1)',
    '0 175px 200px rgba(0, 0, 0, 0.1)',
    '0 185px 210px rgba(0, 0, 0, 0.1)',
    '0 195px 220px rgba(0, 0, 0, 0.1)',
    '0 205px 230px rgba(0, 0, 0, 0.1)',
  ],
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          fontWeight: 500,
        },
        contained: {
          boxShadow: 'none',
          '&:hover': {
            boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
          },
        },
        outlined: {
          borderWidth: 1.5,
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
          overflow: 'hidden',
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            borderRadius: 8,
          },
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          backgroundColor: '#ffffff',
          color: '#212529',
          boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
        },
      },
    },
    MuiDrawer: {
      styleOverrides: {
        paper: {
          backgroundColor: '#ffffff',
          color: '#212529',
          borderRight: '1px solid #e9ecef',
        },
      },
    },
  },
});

export default theme;