import React from 'react';

const App = () => {
  return (
    <>
        <nav class="navbar navbar-expand-lg bg-body-tertiary">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">Navbar</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNavAltMarkup" aria-controls="navbarNavAltMarkup" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
            <div class="navbar-nav">
                <a class="nav-link active" aria-current="page" href="#">Home</a>
                <a class="nav-link" href="#">Features</a>
                <a class="nav-link" href="#">Pricing</a>
                <a class="nav-link disabled" aria-disabled="true">Disabled</a>
            </div>
            </div>
        </div>
        </nav>
        <div class="calendar">
        <div class="timeline" id="hours">
        </div>
        <div class="days">
            <div class="day mon">
            <div class="date">
                <p class="date-num">9</p>
                <p class="date-day">Mon</p>
            </div>
            <div class="events" id="events-mon">

            </div>
            </div>
            <div class="day tues">
            <div class="date">
                <p class="date-num">10</p>
                <p class="date-day">Tues</p>
            </div>
            <div class="events">
            </div>
            </div>
            <div class="day wed">
            <div class="date">
                <p class="date-num">11</p>
                <p class="date-day">Wed</p>
            </div>
            <div class="events">
            </div>
            </div>
            <div class="day thurs">
            <div class="date">
                <p class="date-num">12</p>
                <p class="date-day">Thurs</p>
            </div>
            <div class="events">
            </div>
            </div>
            <div class="day fri">
            <div class="date">
                <p class="date-num">13</p>
                <p class="date-day">Fri</p>
            </div>
            <div class="events">
            </div>
            </div>
        </div>
        </div>
    </>
  );
};

export default App;
