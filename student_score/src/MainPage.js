import React, {useEffect, useState} from 'react';
import './static/css/main_page.css';


function MainPage(props) {

    return (
        <body>
        <main>
            <section className="hero">
                <div className="hero-text">
                    <h2>Welcome to Students Rating</h2>
                    <p>Our web app allows teachers to easily rate and track the progress of their students.</p>
                </div>

            </section>
            <h2>Features</h2>

            <section className="features">
                <div className="feature-box">
                    <i className="fas fa-users"></i>
                    <h3>Manage Students</h3>
                    <p>Easily manage all your students in one place, add new students, view progress reports, and
                        more.</p>
                </div>
                <div className="feature-box">
                    <i className="fas fa-tasks"></i>
                    <h3>Assignments</h3>
                    <p>Create and assign homework and classwork to your students, and view their progress and
                        grades.</p>
                </div>
                <div className="feature-box">
                    <i className="fas fa-chart-line"></i>
                    <h3>Track Progress</h3>
                    <p>View detailed reports and analytics on your students' progress, and identify areas where they may
                        need additional support.</p>
                </div>
            </section>
        </main>
        <footer>
            <div className="footer-content">
                <p> Students Rating </p>
                <p>&copy; 2023 Students Rating. All rights reserved.</p>
            </div>
        </footer>
        </body>
);
}
export default MainPage;
