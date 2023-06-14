import { render, screen, waitFor } from '@testing-library/react';
import ScoresTable from './ScoresTable';
import axios from 'axios';

jest.mock('axios'); // Mock axios module

describe('ScoresTable', () => {
  test('fetches and displays ratings when selected number of students changes', async () => {
    // Mock data for successful API response
    const mockData = [
      { name: 'John', score: { name: 'Math', value: 90 } },
      { name: 'Alice', score: { name: 'Math', value: 85 } },
      // ...add more mock data as needed
    ];

    axios.get.mockResolvedValueOnce({ data: mockData }); // Mock axios get() method

    render(<ScoresTable token="mockToken" />);

    await waitFor(() => {
      const ratingItems = screen.getAllByRole('listitem');
      expect(ratingItems).toHaveLength(2); // Assuming there are 2 students in the mockData
      expect(ratingItems[0]).toHaveTextContent('John: 90');
      expect(ratingItems[1]).toHaveTextContent('Alice: 85');
      // ...assertions for other students' ratings
    });
  });


});
