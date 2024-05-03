<div href="/" class="d-flex align-items-center pb-3 mb-3 link-dark text-decoration-none">
    <img src="/static/arch.png" width="300px" height="auto" alt="arch">
</div>

# **Overview**

<div href="/" class="d-flex align-items-center pb-3 mb-3 link-dark text-decoration-none border-bottom"></div>

The lab environment, the service endpoints, and how you interact with the load balancer have been simplified in an effort to focus on concepts.
Understanding the environment, it's topology, and the rudimentary functionality of the <strong><a href="https://github.com/f5devcentral/f5xc-lab-mcn-practical/tree/main/cloudapp" target="_blank">cloud app</a></strong> will help in completing the exercises.

<div style="height:25px"></div>

## **Architecture**

The lab environment contains three distributed sites meshed using the F5 Distributed Cloud Global Network.

<ul class="list-group">
  <li class="list-group-item">
  <img src="/static/aws.png" width="40px" height="auto" class="rounded"> &nbsp;&nbsp;&nbsp;
    <strong>student-awsnet</strong> in Amazon Web Services
  </li>
  <li class="list-group-item">
  <img src="/static/azure.png" width="40px" height="auto" class="rounded"> &nbsp;&nbsp;&nbsp;
  <strong>student-azurenet</strong> in Microsoft Azure
  </li>
  <li class="list-group-item">
  <img src="/static/mcnp-udf.png" width="40px" height="auto"> &nbsp;&nbsp;&nbsp;
  <strong>Lab CE</strong> in UDF 
  </li>
</ul>

<div style="height:25px"></div>

<img src="/static/mcn-prac-arch-base.png" width="auto" height="600px" alt="Arch diagram">

## **Cloud App**

An instance of the <strong><a href="https://github.com/f5devcentral/f5xc-lab-mcn-practical/tree/main/cloudapp" target="_blank">cloud app</a></strong> is hosted in each remote cloud environment.
The cloud app is a simple application that echoes back an HTTP request.
While working through the lab, unless otherwise noted, test results display headers and info **from the request received by the app**.

For testing, you can access an endpoint of each cloud app from your browser.

<p float="left">
<a href="https://aws-cloud-app.mcn-lab.f5demos.com/pretty" target="_blank">
<img src="/static/aws.png" height="100px" width="auto" class="rounded"/>
</a>
<a href="https://azure-cloud-app.mcn-lab.f5demos.com/pretty" target="_blank">
<img src="/static/azure.png" height="100px" width="auto"  class="rounded"/>
</a></p>

<div style="height:25px"></div>

## **Lab Exercises**

Lab exercises will ask you to create configuration in the <strong><a href="https://f5-xc-lab-mcn.console.ves.volterra.io/" target="_blank">lab tenant</a></strong>.
Exercise requirements are listed in a table along with an object type indicator. 

<ul class="list-group">
  <li class="list-group-item">
  <img src="/static/lb-icon.png" width="auto" height="50px"> &nbsp; &nbsp;
    <strong>Load Balancer</strong>
  </li>
  <li class="list-group-item">
  <img src="/static/origin-icon.png" width="auto" height="50px"> &nbsp; &nbsp;
    <strong>Origin Pool</strong>
  </li>
  <li class="list-group-item">
  <img src="/static/route-icon.png" width="auto" height="50px"> &nbsp; &nbsp;
    <strong>Route</strong> 
  </li>
</ul>

<div style="height:25px"></div>

#### **Test Criteria**

To complete lab exercises, you will run tests against the load balancer advertised from the Customer Edge in your UDF site.
You will build this load balancer in the <strong><a href="/lb">first exercise</a></strong>.
All tests will be run from this lab app.

Each test will specify success criteria immediately before the <button id="null" class="btn btn-primary disabled">Test Load Balancer</button> button.

Here are some examples to try. 

```http
GET https://foo.mcn-lab.f5demos.com/ HTTP/1.1

{
  "info": {
    "foo": True
  }
}
```

<div class="left-aligned-button-container">
    <button id="requestBtn1" class="btn btn-primary">👍 Test</button>
</div>
<div id="result1" class="mt-3"></div>
<script>
document.getElementById('requestBtn1').addEventListener('click', () => {
    testHttpRequest('requestBtn1', '/_test1', 'result1');
});
</script>

The test made a request to <strong>https://foo.mcn-lab.f5demos.com</strong>.
The test succeeded because the response contained the ``JSON`` string ``{ "info": { "foo": True }}``.

<div style="height:25px"></div>

```http
GET https://bar.mcn-lab.f5demos.com/ HTTP/1.1

{
  "info": {
    "bar": True
  }
}
```

<div class="left-aligned-button-container">
    <button id="requestBtn2" class="btn btn-primary">👎 Test</button>
</div>
<div id="result2" class="mt-3"></div>
<script>
document.getElementById('requestBtn2').addEventListener('click', () => {
    testHttpRequest('requestBtn2', '/_test2', 'result2');
});
</script>

The test made a request to <strong>https://bar.mcn-lab.f5demos.com</strong>.
The test failed because the response did not contain the ``JSON`` string ``{ "info": { "bar": True}}``.


<div style="height:25px"></div>

#### **Other Tools**

``curl`` and ``jq`` are provided on the UDF <strong>Runner</strong> instance.

```shell
ubuntu@ubuntu:~$ curl -s https://foo.mcn-lab.f5demos.com/ | jq
{
  "info": "bar"
}
```
<div class="alert alert-secondary" role="alert">
  Responses displayed in exercise tests are truncated for readibility.
</div>

<div style="height:25px"></div>

## **Issues**

Use the lab repository <i class="bi bi-github"> </i><strong><a href="https://github.com/f5devcentral/f5xc-lab-mcn-practical/" target="_blank">issue tracker</a></strong> to report bugs, typos, or lab enhancements.

<div href="/" class="d-flex align-items-center pb-3 mb-3 link-dark text-decoration-none border-bottom"></div>

<nav aria-label="labapp nav">
  <ul class="pagination justify-content-end">
    <li class="page-item">
      <a class="page-link" href="/setup">Setup <i class="bi bi-arrow-right-circle-fill"></i></a>
    </li>
  </ul>
</nav>






