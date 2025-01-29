function openDatePicker() {
    document.getElementById('dateInput')._flatpickr.open();
}

function updateDate(selectedDates, dateStr) {
    document.getElementById('dateDisplay').textContent = dateStr;
}

window.onload = function() {
    const today = new Date().toISOString().split('T')[0];
    document.getElementById('dateDisplay').textContent = today;
    flatpickr("#dateInput", {
        defaultDate: today,
        onChange: updateDate,
        dateFormat: "F j, Y",
    });
};