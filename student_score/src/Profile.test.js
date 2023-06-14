import React from 'react';
import { render, screen } from '@testing-library/react';
import axios from 'axios';
import UserListing from './UserListing';

jest.mock('axios');

describe('Profile', () => {
  test('renders user listing correctly for teacher', async () => {
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

  test('renders user listing correctly for student', async () => {
    const mockToken = 'mockToken';
    const mockUsersData = {
      username: 'JaneDoe',
      model: 'Student',
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

    // Check that no edit buttons are rendered for the student
    const editButtons = screen.queryAllByRole('button', { name: 'Edit scores' });
    expect(editButtons.length).toBe(0);
  });
});
