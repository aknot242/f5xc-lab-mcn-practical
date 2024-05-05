// Utility function to get a cookie by name
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

// Utility function to set a cookie
function setCookie(name, value, days) {
    let expires = '';
    if (days) {
        const date = new Date();
        date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
        expires = `; expires=${date.toUTCString()}`;
    }
    document.cookie = `${name}=${value}${expires}; path=/`;
}

function updateScore(requestUrl, status) {
    // Retrieve the current cookie, assume it's base64 encoded, or default to an encoded empty object
    const base64EncodedData = getCookie('mcnp-ac-data') || btoa('{}');
    const cookieStr = atob(base64EncodedData);
    let cookieData = JSON.parse(cookieStr);

    // Check if the 'score' object exists, if not initialize it
    if (!cookieData.score) {
        cookieData.score = {};
    }

    // Update the score object with the result of the current request
    cookieData.score[requestUrl] = status;

    // Convert the updated cookie object back to string, then encode to base64
    const updatedStr = JSON.stringify(cookieData);
    const updatedBase64Data = btoa(updatedStr);

    // Update the cookie with the new base64 encoded data
    setCookie('mcnp-ac-data', updatedBase64Data, 1);
}

function clearScore(requestUrl, status) {
    // Retrieve the current cookie, assume it's base64 encoded, or default to an encoded empty object
    const base64EncodedData = getCookie('mcnp-ac-data') || btoa('{}');
    const cookieStr = atob(base64EncodedData);
    let cookieData = JSON.parse(cookieStr);

    // Clear the score
    cookieData.score = {};

    // Convert the updated cookie object back to string, then encode to base64
    const updatedStr = JSON.stringify(cookieData);
    const updatedBase64Data = btoa(updatedStr);

    // Update the cookie with the new base64 encoded data
    setCookie('mcnp-ac-data', updatedBase64Data, 1); 
}

async function testHttpRequest(buttonId, requestUrl, resultDivId, buttonTxt) {
    const button = document.getElementById(buttonId);
    const resultDiv = document.getElementById(resultDivId);

    // Add spinner to button and disable it
    button.innerHTML = `Testing...<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>`;
    button.disabled = true;
    
    try {
        const response = await axios.get(requestUrl);
        if (response.data.status === 'success') {
            const prettyJson = JSON.stringify(response.data.data, null, 4);
            resultDiv.innerHTML = `<div class="alert alert-success"><b>Request Succeeded:</b><br><pre class="hljs language-json rounded"><code>${prettyJson}</code></pre></div>`;
            updateScore(requestUrl, 'pass');
        } else {
            const errJson = JSON.stringify(response.data.error, null, 4);
            resultDiv.innerHTML = `<div class="alert alert-danger"><b>Request Failed:</b><br><pre class="hljs rounded"><code>${errJson}</code></pre></div>`;
            updateScore(requestUrl, 'fail');
        }
    } catch (error) {
        resultDiv.innerHTML = `<div class="alert alert-danger">Error: ${error.message}</div>`;
        updateScore(requestUrl, 'fail');
    } finally {
        // Restore original button text and remove spinner
        button.innerHTML = buttonTxt;
        button.disabled = false;
        resultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
}

async function testPostRequest(buttonId, requestUrl, resultDivId, inputDataId, buttonTxt) {
    const button = document.getElementById(buttonId);
    const resultDiv = document.getElementById(resultDivId);
    const inputData = document.getElementById(inputDataId).value;


    // Add spinner and change button text
    button.innerHTML = `Testing...<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>`;
    button.disabled = true;

    try {
        const response = await axios.post(requestUrl, { userInput: inputData });
        if (response.data.status === 'success') {
            const prettyJson = JSON.stringify(response.data.data, null, 4);
            resultDiv.innerHTML = `<div class="alert alert-success"><b>Request Succeeded:</b><br><pre class="hljs language-json rounded"><code>${prettyJson}</code></pre></div>`;
            updateScore(requestUrl, 'pass');
        } else {
            const errJson = JSON.stringify(response.data.error, null, 4);
            resultDiv.innerHTML = `<div class="alert alert-danger"><b>Request Failed:</b><br><pre class="hljs rounded"><code>${errJson}</code></pre></div>`;
            updateScore(requestUrl, 'fail');
        }
    } catch (error) {
        resultDiv.innerHTML = `<div class="alert alert-danger">Error: ${error.message}</div>`;
        updateScore(requestUrl, 'fail');
    } finally {
        // Restore original button text
        button.innerHTML = buttonTxt;
        button.disabled = false;
        resultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
}