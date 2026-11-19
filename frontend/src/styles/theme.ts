import { createTheme } from '@mui/material/styles';

// Color palette inspired by villa rental luxury and Mediterranean aesthetics
const colors = {
  // Primary villa teal/blue tones
  primary: {
    50: '#e6f7f7',
    100: '#b3e8e8',
    200: '#80d8d8',
    300: '#4dc9c9',
    400: '#1ab9b9',
    500: '#00a9a9', // Main primary color
    600: '#008989',
    700: '#006969',
    800: '#004949',
    900: '#002929',
  },
  // Secondary warm gold tones
  secondary: {
    50: '#fff9e6',
    100: '#ffefb3',
    200: '#ffe680',
    300: '#ffdc4d',
    400: '#ffd21a',
    500: '#ffc800', // Main secondary color
    600: '#cca000',
    700: '#997800',
    800: '#665000',
    900: '#332800',
  },
  // Neutral grays
  neutral: {
    50: '#fafafa',
    100: '#f5f5f5',
    200: '#eeeeee',
    300: '#e0e0e0',
    400: '#bdbdbd',
    500: '#9e9e9e',
    600: '#757575',
    700: '#616161',
    800: '#424242',
    900: '#212121',
  },
  // Semantic colors
  success: {
    light: '#81c784',
    main: '#4caf50',
    dark: '#388e3c',
  },
  warning: {
    light: '#ffb74d',
    main: '#ff9800',
    dark: '#f57c00',
  },
  error: {
    light: '#e57373',
    main: '#f44336',
    dark: '#d32f2f',
  },
  info: {
    light: '#64b5f6',
    main: '#2196f3',
    dark: '#1976d2',
  },
};

// Typography scale using Inter font
const typography = {
  fontFamily: '"Inter", "Roboto", "Helvetica", "Arial", sans-serif',
  h1: {
    fontSize: '2.5rem',
    fontWeight: 700,
    lineHeight: 1.2,
    letterSpacing: '-0.01562em',
  },
  h2: {
    fontSize: '2rem',
    fontWeight: 700,
    lineHeight: 1.3,
    letterSpacing: '-0.00833em',
  },
  h3: {
    fontSize: '1.75rem',
    fontWeight: 600,
    lineHeight: 1.4,
  },
  h4: {
    fontSize: '1.5rem',
    fontWeight: 600,
    lineHeight: 1.4,
  },
  h5: {
    fontSize: '1.25rem',
    fontWeight: 500,
    lineHeight: 1.5,
  },
  h6: {
    fontSize: '1rem',
    fontWeight: 500,
    lineHeight: 1.6,
  },
  subtitle1: {
    fontSize: '1rem',
    fontWeight: 400,
    lineHeight: 1.75,
  },
  subtitle2: {
    fontSize: '0.875rem',
    fontWeight: 500,
    lineHeight: 1.57,
  },
  body1: {
    fontSize: '1rem',
    fontWeight: 400,
    lineHeight: 1.5,
  },
  body2: {
    fontSize: '0.875rem',
    fontWeight: 400,
    lineHeight: 1.43,
  },
  button: {
    fontSize: '0.875rem',
    fontWeight: 600,
    textTransform: 'none',
  },
  caption: {
    fontSize: '0.75rem',
    fontWeight: 400,
    lineHeight: 1.66,
  },
  overline: {
    fontSize: '0.625rem',
    fontWeight: 700,
    textTransform: 'uppercase',
    letterSpacing: '0.1em',
  },
};

// Spacing system (4px base grid)
const spacing = (factor: number) => `${factor * 4}px`;

// Create MUI theme
export const theme = createTheme({
  palette: {
    mode: 'light',
    primary: {
      main: colors.primary[500],
      light: colors.primary[300],
      dark: colors.primary[700],
      contrastText: '#ffffff',
    },
    secondary: {
      main: colors.secondary[500],
      light: colors.secondary[300],
      dark: colors.secondary[700],
      contrastText: '#000000',
    },
    background: {
      default: colors.neutral[50],
      paper: '#ffffff',
    },
    text: {
      primary: colors.neutral[900],
      secondary: colors.neutral[700],
      disabled: colors.neutral[500],
    },
    divider: colors.neutral[200],
    success: colors.success,
    warning: colors.warning,
    error: colors.error,
    info: colors.info,
    grey: colors.neutral,
  },
  typography,
  shape: {
    borderRadius: 8,
  },
  spacing: 4, // 4px base unit
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          padding: '8px 16px',
        },
        contained: {
          boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
          '&:hover': {
            boxShadow: '0 4px 8px rgba(0, 0, 0, 0.15)',
          },
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 12,
          boxShadow: '0 2px 8px rgba(0, 0, 0, 0.08)',
          overflow: 'hidden',
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          boxShadow: '0 2px 4px rgba(0, 0, 0, 0.05)',
        },
      },
    },
    MuiDrawer: {
      styleOverrides: {
        paper: {
          borderRight: `1px solid ${colors.neutral[200]}`,
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
  },
});

// Export design tokens for use in components
export const designTokens = {
  colors,
  typography,
  spacing,
  shadows: {
    small: '0 2px 4px rgba(0, 0, 0, 0.1)',
    medium: '0 4px 8px rgba(0, 0, 0, 0.12)',
    large: '0 8px 16px rgba(0, 0, 0, 0.15)',
    xlarge: '0 12px 24px rgba(0, 0, 0, 0.18)',
  },
  breakpoints: {
    xs: 0,
    sm: 600,
    md: 900,
    lg: 1200,
    xl: 1536,
  },
  zIndex: {
    appBar: 1100,
    drawer: 1200,
    modal: 1300,
    snackbar: 1400,
    tooltip: 1500,
  },
};

export default theme;