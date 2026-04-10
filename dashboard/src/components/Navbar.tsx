import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';

interface NavbarProps {
  darkMode: boolean;
  onToggleDarkMode: () => void;
}

const links = [
  { to: '/', label: 'Dashboard' },
  { to: '/tasks', label: 'Tasks' },
  { to: '/groups', label: 'Grupos' },
  { to: '/memory', label: 'Memoria' },
  { to: '/monitoring', label: 'Monitoring' },
  { to: '/scheduler', label: 'Scheduler' },
  { to: '/settings', label: 'Settings' },
];

const Navbar: React.FC<NavbarProps> = ({ darkMode, onToggleDarkMode }) => {
  const [mobileOpen, setMobileOpen] = useState(false);

  const linkClass = ({ isActive }: { isActive: boolean }) =>
    `px-3 py-2 rounded-md text-sm font-medium transition-colors ${
      isActive
        ? 'bg-indigo-700 text-white'
        : 'text-gray-300 hover:bg-gray-700 hover:text-white'
    }`;

  return (
    <nav className="bg-gray-800 shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center">
            <span className="text-white text-xl font-bold">
              🤖 Agencia IA Dashboard
            </span>
            <div className="hidden md:flex ml-10 space-x-2">
              {links.map((link) => (
                <NavLink key={link.to} to={link.to} className={linkClass} end={link.to === '/'}>
                  {link.label}
                </NavLink>
              ))}
            </div>
          </div>

          <div className="flex items-center space-x-3">
            <button
              onClick={onToggleDarkMode}
              className="p-2 rounded-md text-gray-300 hover:text-white hover:bg-gray-700 transition-colors"
              aria-label="Toggle dark mode"
            >
              {darkMode ? '☀️' : '🌙'}
            </button>
            <button
              onClick={() => setMobileOpen(!mobileOpen)}
              className="md:hidden p-2 rounded-md text-gray-300 hover:text-white hover:bg-gray-700"
              aria-label="Open menu"
            >
              {mobileOpen ? '✕' : '☰'}
            </button>
          </div>
        </div>
      </div>

      {mobileOpen && (
        <div className="md:hidden px-2 pt-2 pb-3 space-y-1">
          {links.map((link) => (
            <NavLink
              key={link.to}
              to={link.to}
              className={linkClass}
              end={link.to === '/'}
              onClick={() => setMobileOpen(false)}
            >
              <div className="block">{link.label}</div>
            </NavLink>
          ))}
        </div>
      )}
    </nav>
  );
};

export default Navbar;
