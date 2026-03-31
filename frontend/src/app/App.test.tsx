/**
 * App.test.tsx – Basic shell render test.
 *
 * Validates that the application mounts without crashing and the navigation
 * shell is present with the expected links.
 */

import { describe, it, expect } from 'vitest';
import { render, screen } from '@testing-library/react';
import App from '../App';

describe('App shell', () => {
  it('renders the navigation header', () => {
    render(<App />);
    expect(screen.getByText('CIC Mission Manager')).toBeDefined();
  });

  it('renders the Dashboard nav link', () => {
    render(<App />);
    expect(screen.getByRole('link', { name: 'Dashboard' })).toBeDefined();
  });

  it('renders the New Scenario nav link', () => {
    render(<App />);
    expect(screen.getByRole('link', { name: 'New Scenario' })).toBeDefined();
  });

  it('renders the Diagnostics nav link', () => {
    render(<App />);
    expect(screen.getByRole('link', { name: 'Diagnostics' })).toBeDefined();
  });

  it('renders the scenario dashboard page on the default route', () => {
    render(<App />);
    expect(screen.getByText('Scenario Dashboard')).toBeDefined();
  });
});
