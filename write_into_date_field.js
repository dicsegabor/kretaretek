function writeValueIntoInput(inputFieldId, value) {
  const inputField = document.getElementById(inputFieldId);
  if (inputField) {
    inputField.value = value;
  } else {
    console.error("Input field with ID '" + inputFieldId + "' not found.");
  }
}

// Example usage - Assuming argument[0] holds the value you want to write:
writeValueIntoInput("Datum", arguments[0]);
