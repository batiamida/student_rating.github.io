import React from 'react';
import { render, fireEvent, screen } from '@testing-library/react';
import axios from 'axios';
import { useParams } from 'react-router-dom';
import EditScores from './EditScores';

jest.mock('axios');
jest.mock('react-router-dom', () => ({
  ...jest.requireActual('react-router-dom'),
  useParams: jest.fn(),
}));

describe('EditScores', () => {
  beforeEach(() => {
    useParams.mockReturnValue({ id: 'testId' });
  });

  it('fetches score data and allows updating and deleting scores', async () => {
    const mockScoreList = [
      {
        id: 'scoreId1',
        subject: { id: 'subjectId1', name: 'Subject 1' },
        teacher: { id: 'teacherId1', firstName: 'Teacher 1' },
        score: 90,
      },
      {
        id: 'scoreId2',
        subject: { id: 'subjectId2', name: 'Subject 2' },
        teacher: { id: 'teacherId2', firstName: 'Teacher 2' },
        score: 80,
      },
    ];

    const mockTeachers = [
      { id: 'teacherId1', username: 'teacher1' },
      { id: 'teacherId2', username: 'teacher2' },
    ];

    const mockSubjects = [
      { id: 'subjectId1', name: 'Subject 1' },
      { id: 'subjectId2', name: 'Subject 2' },
    ];

    axios.get.mockResolvedValueOnce({ data: mockScoreList });
    axios.get.mockResolvedValueOnce({ data: { teachers: mockTeachers, subjects: mockSubjects } });
    axios.put.mockResolvedValueOnce({});
    axios.delete.mockResolvedValueOnce({});
    axios.post.mockResolvedValueOnce({});

    render(<EditScores token="mockToken" />);

    await screen.findByText('Score List');

    expect(axios.get).toHaveBeenCalledTimes(2);
    expect(axios.get).toHaveBeenCalledWith('http://localhost:5000/scores/testId');

    const teacherNameElement = await screen.findByText(/Teacher Name:\s+Teacher 1/);
    expect(teacherNameElement).toBeInTheDocument();

    expect(screen.getByText('Subject: Subject 1')).toBeInTheDocument();
    expect(screen.getByText('Subject: Subject 2')).toBeInTheDocument();

    const updateButtons = screen.queryAllByText('Update');
    expect(updateButtons.length).toBe(2); // Make sure there are two update buttons

    fireEvent.change(screen.getByDisplayValue('90'), { target: { value: '95' } });
    fireEvent.click(updateButtons[0]); // Select the first update button
    expect(axios.put).toHaveBeenCalledWith(
      'http://localhost:5000/score',
      { score: '95', id: 'scoreId1' },
      { headers: { Authorization: 'Bearer mockToken' } }
    );

    const deleteButtons = screen.queryAllByText('Delete');
    expect(deleteButtons.length).toBe(2); // Make sure there are two delete buttons

    fireEvent.click(deleteButtons[0]); // Select the first delete button
    expect(axios.delete).toHaveBeenCalledWith('http://localhost:5000/score', {
      headers: { Authorization: 'Bearer mockToken' },
      data: { id: 'scoreId1' },
    });
  });


  it('does not add a new score when inputs are missing', async () => {
    const mockTeachers = [
      { id: 'teacherId1', username: 'teacher1' },
      { id: 'teacherId2', username: 'teacher2' },
    ];

    const mockSubjects = [
      { id: 'subjectId1', name: 'Subject 1' },
      { id: 'subjectId2', name: 'Subject 2' },
    ];

    axios.get.mockResolvedValueOnce({ data: [] });
    axios.get.mockResolvedValueOnce({ data: { teachers: mockTeachers, subjects: mockSubjects } });
    axios.post.mockResolvedValueOnce({});

    render(<EditScores token="mockToken" />);

    await screen.findByText('Score List');

    fireEvent.click(screen.getByText('Add Score'));

    expect(axios.post).not.toHaveBeenCalled();
  });
});
