//import { response } from "express";

//  FUNCTION DEFINITIONS
function calculateTimes() { 

    // Update template table with results
    const template = document.getElementById('template').innerHTML;
    const rendered = Mustache.render(template, resultsDict);
    document.getElementById('target').innerHTML = rendered;
  }


function queryDM() {

    const myHeaders = new Headers({
        'x-printed-credit-key': String(number),
        'x-verification-code': String(code)
    });

    //const request = [number, code]

    const requestOptions = {
    method: "GET",
    headers: myHeaders,
    redirect: "follow"
    };

    fetch("http://localhost:3000/api/voucher", requestOptions)
    .then((response) => {
        if (!response.ok) {
            throw new Error("Network response was not ok");
        }
        return response.json();  // Parse the response as JSON
    })
    .then((result) => {
        // Display the result in the 'voucher-result' div
        console.log(result);
        resultsDict['status'] = result.status;
        resultsDict['value'] = result.balance.value;
        resultsDict['currency'] = result.balance.currency;

        // Update template table with results
        const template = document.getElementById('template').innerHTML;
        const rendered = Mustache.render(template, resultsDict);
        document.getElementById('target').innerHTML = rendered;

    })
    .catch((error) => {
        console.error("Fetch error:", error);
        result.innerText = "Error fetching voucher information.";
    });

    // fetch("http://localhost:3000/api/voucher", requestOptions)
    // .then((response) => response.text())
    // .then((result) => console.log(result))
    // .catch((error) => console.error(error));
}


function buttonClick() {

    // Get the input values
    number = numberField.value;
    code = codeField.value;
    captcha = captchaField.value;

    for (i in checkedBox) {
        checkedBox[i] = document.getElementById(supermarkets[i]).checked;
    }

    console.log("number", number);
    console.log("code", code);
    console.log("captcha", captcha);
    console.log("checkedBox", checkedBox);


    // Show the table which has previously been hidden
    table = document.getElementById('target');
    if (table.style.display == 'none') {
        table.style.display = 'block';
    }

    // Query the respective website
    queryDM();

    // Run the calculation
    calculateTimes();
}

// VARIABLE DEFINITIONS
const btn = document.getElementById('btn');
var inputText = document.getElementById('distance');

const supermarkets = ['rewe', 'edeka', 'lidl', 'dm', 'aldi']
const checkedBox = [false, false, false, false, false];

var numberField = document.getElementById('number');
var codeField = document.getElementById('code');
var captchaField = document.getElementById('captcha');

var result = document.getElementById("voucher-result")

var value = null;
var currency = null;
var status = null;

const resultsDict = new Object();
const speeds = [3.1, 18, 24, 19, 18, 10, 12, 18, 15, 16];
const times = [999, 999, 999, 999, 999, 999, 999, 999, 999, 999];
const ranges = [25, 7, 31, 18, 12, 13, 22, 15, 8, 15];
const withinRange = ['Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes', 'Yes'];


// SCRIPT
btn.addEventListener('click', () => buttonClick());
