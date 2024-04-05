function findAndClickElementByText(text) {
  const elements = document.querySelectorAll("*"); // Get all elements (adjust the tag selector if needed)

  for (let i = 0; i < elements.length; i++) {
    if (elements[i].textContent === text) {
      elements[i].click();
      if(document.querySelector("#FoglalkozasId_listbox").getAttribute('aria-hidden') === 'false') {
          elements[i].click();
      }
      return; // Stop searching once you find and click
    }
  }

  console.log(`Element with text "${text}" not found.`);
}

findAndClickElementByText(arguments[0]);
