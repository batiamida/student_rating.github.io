import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import CreateStudent from './CreateStudent';
import axios from 'axios';



jest.mock('axios');

describe('CreateStudent', () => {
  it('renders the form', () => {
    render(<CreateStudent token="mockToken" />);
    expect(screen.getByLabelText('Username:')).toBeInTheDocument();
    expect(screen.getByLabelText('First Name:')).toBeInTheDocument();
    expect(screen.getByLabelText('Last Name:')).toBeInTheDocument();
    expect(screen.getByLabelText('Email:')).toBeInTheDocument();
    expect(screen.getByLabelText('Phone:')).toBeInTheDocument();
    expect(screen.getByLabelText('Password:')).toBeInTheDocument();
  });

  // it('submits the form and makes API call when Save Changes button is clicked', async () => {
  //   const axiosPostMock = jest.fn().mockResolvedValue({ data: {} });
  //   axios.post.mockImplementationOnce(axiosPostMock);
  //
  //   render(<CreateStudent />);
  //
  //   const inputFields = {
  //     username: 'testUsername',
  //     firstName: 'testFirstName',
  //     lastName: 'testLastName',
  //     email: 'testEmail',
  //     phone: 'testPhone',
  //     password: 'testPassword',
  //   };
  //
  //   Object.keys(inputFields).forEach((field) => {
  //     fireEvent.change(screen.getByLabelText(field), {
  //       target: { value: inputFields[field] },
  //     });
  //   });
  //
  //   fireEvent.click(screen.getByText('Save Changes'));
  //
  //   expect(axiosPostMock).toHaveBeenCalledTimes(1);
  //   expect(axiosPostMock).toHaveBeenCalledWith(
  //     'http://127.0.0.1:5000/student',
  //     inputFields,
  //     { headers: { Authorization: 'Bearer mockToken' } }
  //   );
  // });

  it('clears the form fields when Cancel button is clicked', () => {
    render(<CreateStudent token="mockToken" />);

    const inputFields = {
      username: 'testUsername',
      firstName: 'testFirstName',
      lastName: 'testLastName',
      email: 'testEmail',
      phone: 'testPhone',
      password: 'testPassword',
    };

    Object.keys(inputFields).forEach((field) => {
      fireEvent.change(screen.getByTestId(field), {
        target: { value: inputFields[field] },
      });
    });

    fireEvent.click(screen.getByText('Cancel'));

    Object.keys(inputFields).forEach((field) => {
      expect(screen.getByTestId(field)).toHaveValue('');
    });
  });

  it('submits the form after Save Changes clicked', () => {
    const axiosPostMock = jest.fn().mockResolvedValue({ data: {} });
    axios.post.mockImplementationOnce(axiosPostMock);

    render(<CreateStudent token="mockToken" isLoggedIn={false} />);

    fireEvent.click(screen.getByText('Save Changes'));

    expect(axiosPostMock).toHaveBeenCalledTimes(1);
  });
});
