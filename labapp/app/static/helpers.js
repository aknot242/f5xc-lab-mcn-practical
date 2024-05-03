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

async function testHttpRequest(buttonId, requestUrl, resultDivId) {
    const button = document.getElementById(buttonId);
    const resultDiv = document.getElementById(resultDivId);
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
        button.disabled = false;
        resultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  }

  async function testPostRequest(buttonId, requestUrl, resultDivId, inputDataId) {
    const button = document.getElementById(buttonId);
    const resultDiv = document.getElementById(resultDivId);
    const inputData = document.getElementById(inputDataId).value;
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
        button.disabled = false;
        resultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
}
  
function updateScoreCookie(requestUrl, status) {
    let progress = JSON.parse(getCookie('score') || '{}');
    progress[encodeURIComponent(requestUrl)] = status;
    document.cookie = `progress=${encodeURIComponent(JSON.stringify(progress))}; path=/; expires=${new Date(new Date().getTime() + 86400e3).toUTCString()};`;
  }
