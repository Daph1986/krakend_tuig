// ----------------------- Dynamic years  ----------------------- //

function calculateAge(birthDate) {
  const birthYear = birthDate.getFullYear();
  const currentYear = new Date().getFullYear();
  const age = currentYear - birthYear;
  return age;
}

function updateAgeField(date, ageFieldId) {
  let age = calculateAge(date);
  document.getElementById(ageFieldId).innerHTML = age;
}

function updateDevelopmentYears(startYear, fieldId) {
  const currentYear = new Date().getFullYear();
  const yearsSinceStart = currentYear - startYear;
  document.getElementById(fieldId).textContent = yearsSinceStart;
}

var pickerAnakin = new Pikaday({
  field: document.getElementById('birth_date_anakin'),
  yearRange: [2019, new Date().getFullYear()],
  defaultDate: new Date(2019, 0, 1),
  setDefaultDate: true,
  onSelect: function (date) {
    updateAgeField(date, 'age_anakin');
  }
});

var pickerObi = new Pikaday({
  field: document.getElementById('birth_date_obi'),
  yearRange: [2023, new Date().getFullYear()],
  defaultDate: new Date(2023, 0, 1),
  setDefaultDate: true,
  onSelect: function (date) {
    updateAgeField(date, 'age_obi');
  }
});

// Initial update
updateAgeField(new Date(2019, 0, 1), 'age_anakin');
updateAgeField(new Date(2023, 0, 1), 'age_obi');
updateDevelopmentYears(2021, 'development_years');