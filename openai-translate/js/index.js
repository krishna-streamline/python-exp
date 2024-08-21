const fs = require('fs');
const { Parser } = require('json2csv');

// Sample JSON file path
const languages = ['de','en','es','fr','it','nl','pt']
const folder = 'NTS'
const generateCSV = (language,folder) => {
    const jsonFilePath = `../json/${folder}/${language}.json`;

// Read the JSON file
fs.readFile(jsonFilePath, 'utf8', (err, data) => {
  if (err) {
    console.error('Error reading the file:', err);
    return;
  }

  const jsonData = JSON.parse(data);

  // Convert the key-value pairs into an array of objects
  const csvData = Object.entries(jsonData).map(([key, value]) => ({
    LANGUAGE: language,
    APP_NAME: 'NATIVE TICKET SDK',
    MODULE: 'STATIC TEXT',
    LANG_CODE: key,
    VALUE: value,
    VERSION: '1.0'
  }));

  // Create CSV from the JSON
  const json2csvParser = new Parser({ fields: ['LANGUAGE','APP_NAME','MODULE','LANG_CODE','VALUE','VERSION'] });
  const csv = json2csvParser.parse(csvData);

  // Write the CSV to a file
  fs.writeFile(`${language}.csv`, csv, (err) => {
    if (err) {
      console.error('Error writing the CSV file:', err);
    } else {
      console.log('CSV file successfully created');
    }
  });
});
}
languages.forEach((language, index) => {
  generateCSV(language,folder)
});
