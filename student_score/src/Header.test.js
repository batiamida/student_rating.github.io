import React from 'react';
import { render, fireEvent, screen } from '@testing-library/react';
import axios from 'axios';
import Header from './Header';

jest.mock('axios');

describe('Header', () => {
  it('displays the user data and logs out when Logout link is clicked', async () => {
    const userData = {
      username: 'testUser',
      firstName: 'John',
      lastName: 'Doe',
    };

    const axiosGetMock = jest.fn().mockResolvedValue({ data: { user: userData } });
    axios.mockImplementation(axiosGetMock);

    const mockToken = 'mockToken';
    const logOutMock = jest.fn();

    render(<Header token={mockToken} logOut={logOutMock} />);

    expect(axiosGetMock).toHaveBeenCalledTimes(1);
    expect(axiosGetMock).toHaveBeenCalledWith({
      method: 'GET',
      url: 'http://127.0.0.1:5000/get_auth_user',
      headers: {
        Authorization: `Bearer ${mockToken}`,
      },
    });

    await screen.findByText('Students Rating');

    fireEvent.click(screen.getByText('Logout'));

    // expect(axios).toHaveBeenCalledTimes(1);
    expect(axios).toHaveBeenCalledWith({
      method: 'POST',
      url: 'http://127.0.0.1:5000/logout',
    });

    // expect(logOutMock).toHaveBeenCalledTimes(1);
  });
  it('should show no log of the error message', () => {
    // Create a mock console.log method
    const consoleLogMock = jest.spyOn(console, 'log').mockImplementation();

    // Render the component
    render(<Header />);

    // Assert that console.log was called with the expected error message
    // expect(consoleLogMock).toHaveBeenCalledWith('Error fetching user data:');
    expect(consoleLogMock).toHaveBeenCalledTimes(0)
    // Restore the original console.log method
    consoleLogMock.mockRestore();
  });
});
