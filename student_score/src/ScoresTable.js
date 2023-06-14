import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './static/css/rating_table.css';

function ScoresTable(props) {
  const [selectedNumber, setSelectedNumber] = useState(1); // State for selected number of students

  const fetchData = async () => {
    try {
      const url = `http://127.0.0.1:5000/score/rating/${selectedNumber}`; // Use selected number in the API URL
      const config = {
        headers: {
          Authorization: `Bearer ${props.token}`,
        },
      };

      const response = await axios.get(url, config);
      const data = response.data;

      subjects.forEach((subject) => {
        console.log(subject);
        const ratings = data.filter((item) => item.score.name === subject);

        const subjectRatings = Array.from(document.querySelectorAll('.col-subject h3')).find(
          (h3) => h3.textContent === subject
        );

        if (subjectRatings) {
          const ul = subjectRatings.nextElementSibling;
          ul.innerHTML = ''; // Clear the contents of the ul element

          ratings.forEach((item) => {
            const li = document.createElement('li');
            li.innerHTML = `<span class="name">${item.name}:</span> <span class="value">${item.score.value}</span>`;
            ul.appendChild(li);
          });
        } else {
          const colSubject = document.createElement('div');
          colSubject.className = 'col-subject';
          const h3 = document.createElement('h3');
          h3.textContent = subject;
          const ul = document.createElement('ul');
          ul.className = 'ratings';

          ratings.forEach((item) => {
            const li = document.createElement('li');
            li.innerHTML = `<span class="name">${item.name}:</span> <span class="value">${item.score.value}</span>`;
            ul.appendChild(li);
          });

          colSubject.appendChild(h3);
          colSubject.appendChild(ul);

          const row = document.querySelector('.row');
          row.appendChild(colSubject);
        }
      });
    } catch (error) {
      console.log(error);
    }
  };

  useEffect(() => {
    fetchData();
  }, [props.token, selectedNumber]);

  const handleInputChange = (event) => {
    setSelectedNumber(Number(event.target.value));
    fetchData();
  };

  const subjects = ['Math', 'English', 'Science'];

  return (
    <div className="container">
      <div className="number-input">
        <label>
          Top{' '}
          <input
            type="number"
            min="1"
            value={selectedNumber}
            onChange={handleInputChange}
          />{' '}
          students
        </label>
      </div>
      <h2>Subject Ratings</h2>
      <div className="row">
        {subjects.map((subject) => (
          <div className="col-subject" key={subject}>
            <h3>{subject}</h3>
            <ul className="ratings"></ul>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ScoresTable;
