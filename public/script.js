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

//  FUNCTION DEFINITIONS

// Function to query the DM API
async function queryDM(number, code) {
    const myHeaders = new Headers({
        'x-printed-credit-key': String(number),
        'x-verification-code': String(code)
    });

    const requestOptions = {
        method: "GET",
        headers: myHeaders,
        redirect: "follow"
    };

    return fetch("http://localhost:3000/api/voucher", requestOptions)
        .then((response) => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.json(); // Parse the response as JSON
        });
}

// Function to query the Edeka API
async function queryEdeka(number, code, captcha) {

    const ean = number.slice(3, 16);
    const serial = number.slice(16, 30);
    const timestamp = new Date().toISOString();

    const myHeaders = new Headers({
        'cvcCode': String(code),
        'ean': String(ean),
        'extendedVersion': true,
        'serial': String(serial),
        'timestamp': String(timestamp)
    });

    console.log(myHeaders)

    const requestOptions = {
        method: "GET",
        headers: myHeaders,
        redirect: "follow"
    };

    return fetch("http://localhost:3000/api/voucher", requestOptions)
        .then((response) => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.json(); // Parse the response as JSON
        });
}

// Function to process the API result and update the frontend
function processVoucherResult(result) {

    console.log(result)

    const resultsDict = {
        status: result.status,
        value: result.balance.value,
        currency: result.balance.currency
    };

    // Update template table with results
    const template = document.getElementById('template').innerHTML;
    const rendered = Mustache.render(template, resultsDict);
    document.getElementById('target').innerHTML = rendered;
}

async function buttonClick() {

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
    results = {}
    if (checkedBox[3] == true) {
        results = await queryDM(number, code);
    }
    if (checkedBox[1] == true) {
        results = await queryEdeka(number, code, captcha)
    }

    processVoucherResult(results);
}

// SCRIPT
btn.addEventListener('click', () => buttonClick());