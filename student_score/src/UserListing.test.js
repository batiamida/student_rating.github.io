import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import axios from 'axios';
import UserListing from './UserListing';

jest.mock('axios');

describe('UserListing', () => {
  test('renders user listing correctly', async () => {
    const mockToken = 'mockToken';
    const mockUsersData = {
      username: 'JohnDoe',
      model: 'Teacher',
    };
    const mockUserList = [
      {
        id: 1,
        firstName: 'John',
        lastName: 'Doe',
        email: 'john.doe@example.com',
      },
      {
        id: 2,
        firstName: 'Jane',
        lastName: 'Doe',
        email: 'jane.doe@example.com',
      },
    ];

    axios.mockResolvedValueOnce({ data: { user: mockUsersData } });
    axios.mockResolvedValueOnce({ data: mockUserList });

    render(<UserListing token={mockToken} />);

    // Wait for the user list to be fetched and displayed
    await screen.findByText(`${mockUserList[0].firstName} ${mockUserList[0].lastName}`);
    expect(screen.getByText(mockUserList[0].email)).toBeInTheDocument();

    expect(screen.getByText(`${mockUserList[1].firstName} ${mockUserList[1].lastName}`)).toBeInTheDocument();
    expect(screen.getByText(mockUserList[1].email)).toBeInTheDocument();

    // Check if the edit button is rendered for the teacher
    const editButtons = screen.getAllByRole('button', { name: 'Edit scores' });
    expect(editButtons.length).toBe(2);
  });

  test('clicking on the edit button redirects to the correct URL', async () => {
    const mockToken = 'mockToken';
    const mockUsersData = {
      username: 'JohnDoe',
      model: 'Teacher',
    };
    const mockUserList = [
      {
        id: 1,
        firstName: 'John',
        lastName: 'Doe',
        email: 'john.doe@example.com',
      },
    ];

    axios.mockResolvedValueOnce({ data: { user: mockUsersData } });
    axios.mockResolvedValueOnce({ data: mockUserList });

    // Mock window.location.href
    delete window.location;
    window.location = { href: '' };

    render(<UserListing token={mockToken} />);

    // Wait for the user list to be fetched and displayed
    await screen.findByText(`${mockUserList[0].firstName} ${mockUserList[0].lastName}`);

    const editButtons = screen.getAllByRole('button', { name: 'Edit scores' });
    const editButton = editButtons[0];

    fireEvent.click(editButton);

    expect(window.location.href).toBe(`/edit_scores/${mockUserList[0].id}`);
  });
});
