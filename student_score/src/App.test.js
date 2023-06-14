import React from 'react';
import { render } from '@testing-library/react';
import App from './App';

test('renders the Login component when there is no token', () => {
  const { getByText } = render(<App />);
  // eslint-disable-next-line testing-library/prefer-screen-queries
  const loginElement = getByText(/Login/i);
  expect(loginElement).toBeInTheDocument();
});
