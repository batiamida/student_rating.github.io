import { render, screen } from '@testing-library/react';
import MainPage from './MainPage';

describe('MainPage component', () => {
  it('should render the welcome message', () => {
    render(<MainPage />);
    const welcomeMessage = screen.getByText(/Welcome to Students Rating/i);
    expect(welcomeMessage).toBeInTheDocument();
  });


it('should render the footer content', () => {
  render(<MainPage />);
  const footerContent = screen.getAllByText(/Students Rating/i);
  expect(footerContent).toHaveLength(3); // Adjust the expected length based on the number of occurrences
});

});
