function setCookie(name, value, days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days*24*60*60*1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "") + expires + "; path=/";
}

function getCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0; i < ca.length; i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
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
            resultDiv.innerHTML = `<div class="alert alert-success"><b>Request Succeeded:</b><br><pre><code class="hljs rounded">${prettyJson}</code></pre></div>`;
            updateScoreCookie(requestUrl, 'pass');
        } else {
            const errJson = JSON.stringify(response.data.error, null, 4);
            resultDiv.innerHTML = `<div class="alert alert-danger"><b>Request Failed:</b><br><pre><code class="hljs rounded">${errJson}</code></pre></div>`;
            updateScoreCookie(requestUrl, 'fail');
        }
    } catch (error) {
        resultDiv.innerHTML = `<div class="alert alert-danger">Error: ${error.message}</div>`;
        updateScoreCookie(requestUrl, 'fail');
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
    button.innerHTML = `<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>${buttonTxt}`;
    button.disabled = true;

    try {
        const response = await axios.post(requestUrl, { userInput: inputData });
        if (response.data.status === 'success') {
            const prettyJson = JSON.stringify(response.data.data, null, 4);
            resultDiv.innerHTML = `<div class="alert alert-success"><b>Request Succeeded:</b><br><pre><code class="hljs rounded">${prettyJson}</code></pre></div>`;
            updateScoreCookie(requestUrl, 'pass');
        } else {
            const errJson = JSON.stringify(response.data.error, null, 4);
            resultDiv.innerHTML = `<div class="alert alert-danger"><b>Request Failed:</b><br><pre><code class="hljs rounded">${errJson}</code></pre></div>`;
            updateScoreCookie(requestUrl, 'fail');
        }
    } catch (error) {
        resultDiv.innerHTML = `<div class="alert alert-danger">Error: ${error.message}</div>`;
        updateScoreCookie(requestUrl, 'fail');
    } finally {
        // Restore original button text
        button.innerHTML = buttonTxt;
        button.disabled = false;
        resultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
}
  
  function updateScoreCookie(requestUrl, status) {
    // Get the current cookie, decode it, and parse it as JSON
    const currentCookie = decodeURIComponent(getScoreCookie('score') || '%7B%7D'); // Ensure the default value is an encoded empty JSON object
    let progress = JSON.parse(currentCookie);
    progress[encodeURIComponent(requestUrl)] = status;
    document.cookie = `score=${encodeURIComponent(JSON.stringify(progress))}; path=/; expires=${new Date(new Date().getTime() + 86400e3).toUTCString()};`;
  }
  
  function getScoreCookie(name) {
    let cookieArray = document.cookie.split(';');
    for(let i = 0; i < cookieArray.length; i++) {
      let cookiePair = cookieArray[i].split('=');
      if(name == cookiePair[0].trim()) {
        return cookiePair[1];
      }
    }
    return null;
  }
