import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useParams } from 'react-router-dom';
import './static/css/EditScores.css';

function EditScores(props) {
  const [scoreList, setScoreList] = useState([]);
  const { id } = useParams();
  const [newScores, setNewScores] = useState([]);
  const [teachers, setTeachers] = useState([]);
  const [subjects, setSubjects] = useState([]);

  useEffect(() => {
    const fetchScoreData = async () => {
      try {
        const response = await axios.get(`http://localhost:5000/scores/${id}`);
        const data = response.data;
        setScoreList(data);
      } catch (error) {
        console.error(error);
      }
    };

    fetchScoreData();
  }, [id]);

    useEffect(() => {
    const fetchSubjectsAndTeachers = async () => {
      try {
        const response = await axios.get('http://localhost:5000/subjects_and_teachers', {
          headers: { Authorization: `Bearer ${props.token}` },
        });
        const { teachers, subjects } = response.data;
        setTeachers(teachers);
        setSubjects(subjects);
      } catch (error) {
        console.error(error);
      }
    };

    fetchSubjectsAndTeachers();
  }, [props.token]);

  const handleUpdate = (scoreId) => {
    const inputElement = document.querySelector(`#score-input-${scoreId}`);
    const updatedValue = inputElement.value;

    axios.put(
      `http://localhost:5000/score`,
      { score: updatedValue, id: scoreId },
      { headers: { Authorization: `Bearer ${props.token}` } }
    )
  };


  const handleDelete = (scoreId) => {
    const inputElement = document.querySelector(`#score-input-${scoreId}`);
    const updatedValue = inputElement.value;

    axios.delete(
      `http://localhost:5000/score`,
      { headers: { Authorization: `Bearer ${props.token}` },
              data: {id: scoreId}},
    )

    window.location.reload();
  };

  const handleAddScore = async () => {
    const newTeacherInput = document.querySelector('#new-teacher-input');
    const newSubjectInput = document.querySelector('#new-subject-input');
    const newScoreInput = document.querySelector('#new-score-input');
    const teacherName = newTeacherInput.options[newTeacherInput.selectedIndex].text.trim();

    const subjectName = newSubjectInput.options[newSubjectInput.selectedIndex].text.trim();
    const scoreValue = newScoreInput.value;

    if (teacherName && subjectName && scoreValue !== '') {


      try {
        const response = await axios.post(
          'http://localhost:5000/score_by_names',
            {teacher_name: teacherName, subject_name: subjectName, score: scoreValue, student_id: id},
          { headers: { Authorization: `Bearer ${props.token}` } }
        );

        window.location.reload();
        const { teachers, subjects } = response.data;

        const selectedTeacher = teachers.find((teacher) => teacher.firstName === teacherName);
        const selectedSubject = subjects.find((subject) => subject.name === subjectName);

        if (selectedTeacher && selectedSubject) {
          const newScore = {
            id: Math.random().toString(),
            subject: { id: selectedSubject.id, name: selectedSubject.name },
            teacher: { id: selectedTeacher.id, firstName: selectedTeacher.firstName },
            score: parseFloat(scoreValue),
          };

          setScoreList([...scoreList, newScore]);

          newTeacherInput.value = '';
          newSubjectInput.value = '';
          newScoreInput.value = '';
        }

      } catch (error) {
        console.error(error);
      }
    }
  };




  return (
    <div className="score-list">
      <h2>Score List</h2>
      {scoreList.map((score, index) => (
        <div key={index} className="score-item">
          <h3>Subject: {score.subject.name}</h3>
          <ul>
            <li>
              <strong>Teacher Name: {score.teacher.firstName}</strong>
            </li>
            <li>
              <strong>Score:</strong>
              <div className="score-input-container">
                <input
                  type="number"
                  defaultValue={score.score}
                  id={`score-input-${score.id}`}
                  className="score-input"
                />
              </div>
            </li>
          </ul>
          <div className="score-actions">
            <button onClick={() => handleUpdate(score.id)} className="edit-button">
              Update
            </button>
            <button onClick={() => handleDelete(score.id)} className="delete-button">
              Delete
            </button>
          </div>
        </div>
      ))}
      <div className="score-item">
        <h3>New Score</h3>
        <ul>
          <li>
            <strong>Teacher:</strong>
            <div className="score-input-container">
              <select id="new-teacher-input" className="score-input">
                <option value="">Select teacher</option>
                {teachers.map((teacher) => (
                  <option key={teacher.id} value={teacher.id}>
                    {teacher.username}
                  </option>
                ))}
              </select>
            </div>
          </li>
          <li>
            <strong>Subject:</strong>
            <div className="score-input-container">
              <select id="new-subject-input" className="score-input">
                <option value="">Select subject</option>
                {subjects.map((subject) => (
                  <option key={subject.id} value={subject.id}>
                    {subject.name}
                  </option>
                ))}
              </select>
            </div>
          </li>
          <li>
            <strong>Score:</strong>
            <div className="score-input-container">
              <input
                type="number"
                placeholder="Enter score"
                id="new-score-input"
                className="score-input"
              />
            </div>
          </li>
        </ul>
        <div className="score-actions">
          <button onClick={() => handleAddScore()} className="add-score-button">
            Add Score
          </button>
        </div>
      </div>
    </div>
  );


}

export default EditScores;
