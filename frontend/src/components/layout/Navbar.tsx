'use client';

import { useState } from 'react';
import {
  AppBar,
  Toolbar,
  IconButton,
  Typography,
  Box,
  Avatar,
  Menu,
  MenuItem,
  Divider,
  Badge,
} from '@mui/material';
import {
  Menu as MenuIcon,
  Notifications,
  Search,
  AccountCircle,
  Logout,
  Person,
} from '@mui/icons-material';
import { useAuth } from '@/lib/auth/auth';
import { useRouter } from 'next/navigation';

interface NavbarProps {
  onMenuClick?: () => void;
}

export default function Navbar({ onMenuClick }: NavbarProps) {
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const { user, logout } = useAuth();
  const router = useRouter();

  const handleMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleProfileClick = () => {
    handleMenuClose();
    // Navigate to profile page (to be implemented)
  };

  const handleLogoutClick = () => {
    handleMenuClose();
    logout();
    router.push('/login');
  };

  return (
    <AppBar 
      position="static" 
      elevation={0}
      sx={{ 
        backgroundColor: 'white', 
        color: 'text.primary',
        borderBottom: '1px solid',
        borderColor: 'divider',
      }}
    >
      <Toolbar>
        <IconButton
          edge="start"
          color="inherit"
          aria-label="menu"
          onClick={onMenuClick}
          sx={{ mr: 2, display: { md: 'none' } }}
        >
          <MenuIcon />
        </IconButton>

        <Box sx={{ display: 'flex', alignItems: 'center', flexGrow: 1 }}>
          <Typography
            variant="h6"
            component="div"
            sx={{ 
              fontWeight: 600, 
              background: 'linear-gradient(135deg, #2c3e50 0%, #1976d2 100%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              backgroundClip: 'text',
            }}
          >
            CV Villas Agent Assist
          </Typography>
          <Box sx={{ flexGrow: 1 }} />
          
          <IconButton color="inherit" sx={{ mr: 1 }}>
            <Search />
          </IconButton>
          
          <IconButton color="inherit" sx={{ mr: 1 }}>
            <Badge badgeContent={3} color="error">
              <Notifications />
            </Badge>
          </IconButton>
          
          <Box sx={{ display: 'flex', alignItems: 'center', ml: 2 }}>
            <Avatar
              sx={{ 
                width: 36, 
                height: 36, 
                bgcolor: 'primary.main',
                cursor: 'pointer',
              }}
              onClick={handleMenuOpen}
            >
              {user?.name?.charAt(0) || 'A'}
            </Avatar>
            <Typography variant="body2" sx={{ ml: 2, display: { xs: 'none', sm: 'block' } }}>
              {user?.name || 'Guest'}
              <Typography variant="caption" display="block" color="text.secondary">
                {user?.role?.toUpperCase()}
              </Typography>
            </Typography>
          </Box>
        </Box>

        <Menu
          anchorEl={anchorEl}
          open={Boolean(anchorEl)}
          onClose={handleMenuClose}
          PaperProps={{
            sx: { width: 200, maxWidth: '100%' },
          }}
        >
          <MenuItem onClick={handleProfileClick}>
            <Person fontSize="small" sx={{ mr: 2 }} />
            Profile
          </MenuItem>
          <Divider />
          <MenuItem onClick={handleLogoutClick}>
            <Logout fontSize="small" sx={{ mr: 2 }} />
            Logout
          </MenuItem>
        </Menu>
      </Toolbar>
    </AppBar>
  );
}
