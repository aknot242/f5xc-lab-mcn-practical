<div href="/" class="d-flex align-items-center pb-3 mb-3 link-dark text-decoration-none">
    <img src="https://raw.githubusercontent.com/f5devcentral/f5xc-lab-mcn-practical/main/labapp/app/static/load-balancing.png" width="300px" height="auto" alt="intro">
</div>

# **Load Balancing**

<div href="/" class="d-flex align-items-center pb-3 mb-3 link-dark text-decoration-none border-bottom"></div>

Load balancing is the cornerstone of XC's App Connect functionality.
L7 MCN requires discovering services at one site and making those services available at some other site.
That's accomplished by configuring origin pools and load balancers. 
More complicated configurations (underlay networking, security services, observability, etc.) are built on these primitives.

<div style="height:25px"></div>

### **Exercise 1: AWS Cloud App**

For the initial exercise, make the cloud application running in AWS available to the UDF environment. 
Build an origin pool and load balancer based on the exercise requirements.

<ul class="list-group">
  <li class="list-group-item">
  <img src="/static/origin-icon.png" width="auto" height="50px"> &nbsp; &nbsp;
    The URL for the cloud app hosted in AWS is <a href="https://aws-cloud-app.mcn-lab.f5demos.com">https://aws-cloud-app.mcn-lab.f5demos.com</a>
  </li>
  <li class="list-group-item">
  <img src="/static/origin-icon.png" width="auto" height="50px"> &nbsp; &nbsp;
  The cloud app is only reachable from the <strong>student-awsnet</strong> site.
  </li>
  <li class="list-group-item">
  <img src="/static/origin-icon.png" width="auto" height="50px"> &nbsp; &nbsp;
    The cloud app is TLS only. 
  </li>
  <li class="list-group-item">
  <img src="/static/lb-icon.png" width="auto" height="50px"> &nbsp; &nbsp;
    Use the wildcard cert provided in the shared NS, <strong>mcn-lab-wildcard</strong>, to enable TLS on the LB. 
  </li>
</ul>

<div style="height:25px"></div>

#### **Test Criteria**

```http
GET https://eph-ns.mcn-lab.f5demos.com/ HTTP/1.1
Host: eph-ns.mcn-lab.f5demos.com

{
  "env": "aws",
  ...
}
```

<div class="left-aligned-button-container">
    <button id="requestBtn1" class="btn btn-primary">Test Load Balancer</button>
</div>
<div id="result1" class="mt-3"></div>
<script>
document.getElementById('requestBtn1').addEventListener('click', () => {
    makeHttpRequest('requestBtn1', '/_lb1', 'result1');
});
</script>

<div style="height:25px"></div>

Since this is the first exercise, here are some hints (if you need them).

<div id="hints">
<p>
  <a class="btn btn-primary" data-bs-toggle="collapse" href="#multiCollapseExample1" role="button" aria-expanded="false" aria-controls="multiCollapseExample1">Load Balancer Hint</a>
  <button class="btn btn-primary" type="button" data-bs-toggle="collapse" data-bs-target="#multiCollapseExample2" aria-expanded="false" aria-controls="multiCollapseExample2">Origin Pool Hint</button>
  <button class="btn btn-primary" type="button" data-bs-toggle="collapse" data-bs-target="#multiCollapseExample3" aria-expanded="false" aria-controls="multiCollapseExample3">Origin Server Hint</button>
</p>
<div class="row">

  <div class="collapse multi-collapse" id="multiCollapseExample1" data-bs-parent="#hints">
    <div class="">
      <img src="/static/load-balancer1.png" width="800px" height="auto" alt="temp">
      <img src="/static/load-balancer2.png" width="800px" height="auto" alt="temp">
    </div>
  </div>


  <div class="collapse multi-collapse" id="multiCollapseExample2" data-bs-parent="#hints">
    <div class="">
      <img src="/static/origin-pool.png" width="800px" height="auto" alt="temp">
    </div>
  </div>


  <div class="collapse multi-collapse" id="multiCollapseExample3" data-bs-parent="#hints">
    <div class="">
      <img src="/static/origin-server.png" width="800px" height="auto" alt="temp">
    </div>
  </div>

</div>
</div>

<div  style="height:25px" class="d-flex align-items-center pb-3 mb-3 link-dark text-decoration-none border-bottom"></div>

### **Exercise 2: Azure Cloud App**

For the second exercise, make the cloud application running in Azure available to the UDF environment.
Create a new origin pool for the Azure cloud app. Reuse your load balancer. 


<ul class="list-group">
  <li class="list-group-item">
  <img src="/static/origin-icon.png" width="auto" height="50px"> &nbsp; &nbsp;
      The URL for the cloud app hosted in Azure is <a href="https://azure-cloud-app.mcn-lab.f5demos.com">https://aws-cloud-app.mcn-lab.f5demos.com</a> 
  </li>
  <li class="list-group-item">
  <img src="/static/origin-icon.png" width="auto" height="50px"> &nbsp; &nbsp;
    The cloud app is only reachable from the <strong>student-azurenet</strong> site.
  </li>
  <li class="list-group-item">
  <img src="/static/origin-icon.png" width="auto" height="50px"> &nbsp; &nbsp;
    The cloud app is TLS only. 
  </li>
</ul>

<div style="height:25px"></div>

#### **Test Criteria**

```http
GET https://eph-ns.mcn-lab.f5demos.com/ HTTP/1.1
Host: eph-ns.mcn-lab.f5demos.com

{
  "env": "azure",
  ...
}
```

<div class="left-aligned-button-container">
    <button id="requestBtn2" class="btn btn-primary">Test Load Balancer</button>
</div>
<div id="result2" class="mt-3"></div>
<script>
document.getElementById('requestBtn2').addEventListener('click', () => {
    makeHttpRequest('requestBtn2', '/_lb2', 'result2');
});
</script>

<div  style="height:25px" class="d-flex align-items-center pb-3 mb-3 link-dark text-decoration-none border-bottom"></div>

After completing both exercises, move on to the <strong><a href="/route" class="alert-link">routing</a></strong> exercise.

