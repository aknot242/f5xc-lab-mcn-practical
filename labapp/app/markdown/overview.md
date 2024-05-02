<div href="/" class="d-flex align-items-center pb-3 mb-3 link-dark text-decoration-none">
    <img src="/static/arch.png" width="300px" height="auto" alt="arch">
</div>

# **Overview**

<div href="/" class="d-flex align-items-center pb-3 mb-3 link-dark text-decoration-none border-bottom"></div>

The lab environment, the application endpoints, and how you interact with the load balancer have been simplified in an effort to focus on concepts.
Understanding the environment, it's topology, and the rudimentary functionality of the <strong><a href="https://github.com/f5devcentral/f5xc-lab-mcn-practical/tree/main/cloudapp" target="_blank">cloud app</a></strong> will help in completing the exercises.

<div style="height:25px"></div>

## **Architecture**

The lab environment contains three distributed sites meshed using the F5 Distributed Cloud Global Network.

<div style="height:25px"></div>

<ul class="list-group">
  <li class="list-group-item">
  <img src="/static/mcnp-aws.png" width="auto" height="30px"> &nbsp;&nbsp;
    <strong>student-awsnet</strong> in Amazon Web Services
  </li>
  <li class="list-group-item">
  <img src="/static/mcnp-azure.png" width="auto" height="30px"> &nbsp;&nbsp;&nbsp;
  <strong>student-azurenet</strong> in Microsoft Azure
  </li>
  <li class="list-group-item">
  <img src="/static/mcnp-udf.png" width="auto" height="30px"> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <strong>Lab CE</strong> in UDF 
  </li>
</ul>

<div style="height:25px"></div>

<img src="/static/mcn-prac-arch-base.png" width="auto" height="600px" alt="Arch diagram">

## **Cloud App**

An instance of the <strong><a href="https://github.com/f5devcentral/f5xc-lab-mcn-practical/tree/main/cloudapp" target="_blank">cloud app</a></strong> is hosted in each remote cloud environment.
The cloud app is a simple application that echoes back an HTTP request.
While working through the lab, unless otherwise noted, the test results are displaying the headers and info **from the request received by the app**.

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
To complete a lab exercise, you will run a test against the load balancer advertised from the Customer Edge in your UDF site.
Tests are integrated in this lab app.

<div style="height:25px"></div>

#### **Test Criteria**

Exercises will specify thier success criteria along with the test.

Here are some examples to try. 

```http
GET https://foo.f5demos.com/ HTTP/1.1

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
    makeHttpRequest('requestBtn1', '/_test1', 'result1');
});
</script>

The test made a request to <strong>https://foo.f5demos.com</strong>.
The test succeeded because the response contained the ``JSON`` string ``{ "info": { "foo": True }}``.

<div style="height:25px"></div>

```http
GET https://bar.f5demos.com/ HTTP/1.1

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
    makeHttpRequest('requestBtn2', '/_test2', 'result2');
});
</script>

The test made a request to <strong>https://bar.f5demos.com</strong>.
The test failed because the response did not contain the ``JSON`` string ``{ "info": { "bar": True}}``.


<div style="height:25px"></div>

#### **Other Tools**

``curl`` and ``jq`` are provided on the UDF "Runner" instance.

```shell
ubuntu@ubuntu:~$ curl -s https://foo.mcn-lab.f5demos.com/ | jq
{
  "info": "bar"
}
```


Note that responses displayed in exercise tests are truncated for readibility.

<div href="/" class="d-flex align-items-center pb-3 mb-3 link-dark text-decoration-none border-bottom"></div>

Next, visit the <strong><a href="/setup" >setup page</a></strong> before starting the exercises.






