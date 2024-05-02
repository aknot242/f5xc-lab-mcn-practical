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

async function makeHttpRequest(buttonId, requestUrl, resultDivId) {
  const button = document.getElementById(buttonId);
  const resultDiv = document.getElementById(resultDivId);
  button.disabled = true;
  try {
      const response = await axios.get(requestUrl);
      if (response.data.status === 'success') {
          const prettyJson = JSON.stringify(response.data.data, null, 4);
          resultDiv.innerHTML = `<div class="alert alert-success"><b>Request Succeeded:</b><br><pre><code>${prettyJson}</code></pre></div>`;
      } else {
          const errJson = JSON.stringify(response.data.error, null, 4);
          resultDiv.innerHTML = `<div class="alert alert-danger"><b>Request Failed:</b><br><pre><code>${errJson}</code></pre></div>`;
      }
  } catch (error) {
      resultDiv.innerHTML = `<div class="alert alert-danger">Error: ${error.message}</div>`;
  } finally {
      button.disabled = false;
      resultDiv.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }
}
