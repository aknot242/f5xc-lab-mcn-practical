<div href="/" class="d-flex align-items-center pb-3 mb-3 link-dark text-decoration-none">
    <img src="/static/header.png" width="300px" height="auto" alt="intro">
</div>

# **Header Manipulation**

<div href="/" class="d-flex align-items-center pb-3 mb-3 link-dark text-decoration-none border-bottom"></div>

<div style="height:25px"></div>

### **Exercise 1: Add/Remove**

HERE

<div class="left-aligned-button-container">
    <button id="requestBtn2" class="btn btn-primary">Test Load Balancer</button>
</div>
<div id="result2" class="mt-3"></div>
<script>
    document.getElementById('requestBtn2').addEventListener('click', async () => {
        const resultDiv = document.getElementById('result2');
        try {
            const response = await axios.get('/_head1');
            if(response.data.status === 'success') {
                const prettyJson = JSON.stringify(response.data.data, null, 4);
                resultDiv.innerHTML = `<pre class="alert alert-success"><code>${prettyJson}</code></pre>`;
            } else {
                resultDiv.innerHTML = `<div class="alert alert-danger"><b>Request Failed</b></div>`;
            }
            resultDiv.scrollIntoView({ behavior: 'smooth', block: 'end' }); // Smooth scroll to the resultDiv
        } catch (error) {
            resultDiv.innerHTML = `<div class="alert alert-danger">Error: ${error.message}</div>`;
            resultDiv.scrollIntoView({ behavior: 'smooth', block: 'end' }); // Smooth scroll to the resultDiv
        }
    });
</script>

<div style="height:25px"></div>

Nice 🚀! If you've completed all the exercises so far, you have a good foundation for how App Connect addresses common L7 MCN scenarios.
In subsequent labs, we'll explore security and observabilty concepts that build on MCN functionality.
Head over to the <a href="/vnet" class="alert-link">Network Connect</a> exercise.

<div style="height:25px"></div>