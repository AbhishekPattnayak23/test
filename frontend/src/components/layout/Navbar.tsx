'use client';

import React, { useState } from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  IconButton,
  Box,
  Avatar,
  Menu,
  MenuItem,
  Divider,
  Badge,
} from '@mui/material';
import {
  Menu as MenuIcon,
  Notifications as NotificationsIcon,
  AccountCircle,
  Logout,
  Settings,
} from '@mui/icons-material';
import Link from 'next/link';
import { useAuth } from '@/lib/auth/auth';

const Navbar: React.FC = () => {
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const [notificationAnchorEl, setNotificationAnchorEl] = useState<null | HTMLElement>(null);
  const { user, logout } = useAuth();

  const handleMenuOpen = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleMenuClose = () => {
    setAnchorEl(null);
  };

  const handleNotificationOpen = (event: React.MouseEvent<HTMLElement>) => {
    setNotificationAnchorEl(event.currentTarget);
  };

  const handleNotificationClose = () => {
    setNotificationAnchorEl(null);
  };

  const handleLogout = () => {
    logout();
    handleMenuClose();
  };

  return (
    <AppBar position="static" elevation={0} sx={{ bgcolor: 'background.paper', borderBottom: 1, borderColor: 'divider' }}>
      <Toolbar>
        <IconButton edge="start" color="inherit" aria-label="menu" sx={{ mr: 2, display: { md: 'none' } }}>
          <MenuIcon />
        </IconButton>

        <Box sx={{ flexGrow: 1, display: 'flex', alignItems: 'center' }}>
          <Link href="/dashboard" passHref>
            <Typography
              variant="h6"
              component="div"
              sx={{
                fontWeight: 700,
                color: 'primary.main',
                cursor: 'pointer',
                textDecoration: 'none',
                '&:hover': { opacity: 0.8 },
              }}
            >
              Villa Knowledge Assistant
            </Typography>
          </Link>
          {user && (
            <Typography variant="caption" sx={{ ml: 2, px: 1.5, py: 0.5, bgcolor: 'action.selected', borderRadius: 1 }}>
              {user.role.charAt(0).toUpperCase() + user.role.slice(1)}
            </Typography>
          )}
        </Box>

        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <IconButton
            size="large"
            aria-label="show notifications"
            color="inherit"
            onClick={handleNotificationOpen}
          >
            <Badge badgeContent={3} color="error">
              <NotificationsIcon />
            </Badge>
          </IconButton>

          <IconButton
            size="large"
            aria-label="account of current user"
            aria-controls="menu-appbar"
            aria-haspopup="true"
            onClick={handleMenuOpen}
            color="inherit"
          >
            <Avatar
              sx={{ width: 32, height: 32, bgcolor: user ? 'primary.main' : 'grey.500' }}
              alt={user?.name || 'User'}
            >
              {user?.name?.charAt(0) || <AccountCircle />}
            </Avatar>
          </IconButton>
        </Box>

        <Menu
          id="menu-appbar"
          anchorEl={anchorEl}
          anchorOrigin={{
            vertical: 'bottom',
            horizontal: 'right',
          }}
          keepMounted
          transformOrigin={{
            vertical: 'top',
            horizontal: 'right',
          }}
          open={Boolean(anchorEl)}
          onClose={handleMenuClose}
        >
          {user && (
            <>
              <MenuItem disabled sx={{ opacity: 0.7 }}>
                <Typography variant="body2">
                  Signed in as <strong>{user.email}</strong>
                </Typography>
              </MenuItem>
              <Divider />
              <MenuItem component={Link} href="/profile" onClick={handleMenuClose}>
                <AccountCircle sx={{ mr: 1 }} /> Profile
              </MenuItem>
              <MenuItem component={Link} href="/settings" onClick={handleMenuClose}>
                <Settings sx={{ mr: 1 }} /> Settings
              </MenuItem>
              <Divider />
            </>
          )}
          {user ? (
            <MenuItem onClick={handleLogout}>
              <Logout sx={{ mr: 1 }} /> Logout
            </MenuItem>
          ) : (
            <MenuItem component={Link} href="/login" onClick={handleMenuClose}>
              <AccountCircle sx={{ mr: 1 }} /> Sign In
            </MenuItem>
          )}
        </Menu>

        <Menu
          id="notification-menu"
          anchorEl={notificationAnchorEl}
          anchorOrigin={{
            vertical: 'bottom',
            horizontal: 'right',
          }}
          keepMounted
          transformOrigin={{
            vertical: 'top',
            horizontal: 'right',
          }}
          open={Boolean(notificationAnchorEl)}
          onClose={handleNotificationClose}
        >
          <MenuItem disabled>
            <Typography variant="body2" color="text.secondary">
              Notifications (3 unread)
            </Typography>
          </MenuItem>
          <Divider />
          <MenuItem>
            <Typography variant="body2">
              New expert correction submitted
            </Typography>
            <Typography variant="caption" color="text.secondary" sx={{ ml: 1 }}>
              2h ago
            </Typography>
          </MenuItem>
          <MenuItem>
            <Typography variant="body2">
              System maintenance scheduled
            </Typography>
            <Typography variant="caption" color="text.secondary" sx={{ ml: 1 }}>
              1d ago
            </Typography>
          </MenuItem>
          <MenuItem>
            <Typography variant="body2">
              New knowledge source added
            </Typography>
            <Typography variant="caption" color="text.secondary" sx={{ ml: 1 }}>
              3d ago
            </Typography>
          </MenuItem>
        </Menu>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;