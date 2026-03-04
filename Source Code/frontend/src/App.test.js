import { render, screen } from '@testing-library/react';
import App from './App';

test('renders SmartPick title', () => {
  render(<App />);
  const title = screen.getByText(/SmartPick/i);
  expect(title).toBeInTheDocument();
});