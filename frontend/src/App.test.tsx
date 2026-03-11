import React from 'react';
import { render, screen } from '@testing-library/react';
import App from './App';

test('renders app link', () => {
  render(<App />);
  const linkElement = screen.getByText(/Community Insights Analyzer/i);
  expect(linkElement).toBeInTheDocument();
});
