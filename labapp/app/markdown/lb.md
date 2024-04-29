<div href="/" class="d-flex align-items-center pb-3 mb-3 link-dark text-decoration-none">
    <img src="/static/load-balancing.png" width="300px" height="auto" alt="intro">
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
Build an origin pool and load balancer based on the following criteria:


<div class="form-check">
  <input class="form-check-input" type="checkbox" value="" id="flexCheckDefault" checked>
  <label class="form-check-label" for="flexCheckDefault">
    The URL for the cloud app hosted in AWS is <a href="https://aws-cloud-app.mcn-lab.f5demos.com">https://aws-cloud-app.mcn-lab.f5demos.com</a>  
  </label>
</div>
<div class="form-check">
  <input class="form-check-input" type="checkbox" value="" id="flexCheckDefault" checked>
  <label class="form-check-label" for="flexCheckCDefault">
    The cloud app is only reachable from the "student-awsnet" site.
  </label>
</div>
<div class="form-check">
  <input class="form-check-input" type="checkbox" value="" id="flexCheckDefault" checked>
  <label class="form-check-label" for="flexCheckCDefault">
    The cloud app is TLS enabled.
  </label>
</div>
<div class="form-check">
  <input class="form-check-input" type="checkbox" value="" id="flexCheckDefault" checked>
  <label class="form-check-label" for="flexCheckCDefault">
    Use the wildcard cert provided in the shared NS, "mcn-lab-wildcard", to enable TLS on the LB.
  </label>
</div>
<div class="form-check">
  <input class="form-check-input" type="checkbox" value="" id="flexCheckDefault" checked>
  <label class="form-check-label" for="flexCheckCDefault">
    The load balancer should only be advertised from your CE in UDF. <b>Do not advertise this service on the Internet.</b>
  </label>
</div>


<div style="height:25px"></div>

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

<div style="height:25px"></div>

### **Exercise 2: Azure Cloud App**

For the second exercise, make the cloud application running in Azure available to the UDF environment.
Create a new origin pool for the Azure cloud app. Reuse your load balancer. 

<div class="form-check">
  <input class="form-check-input" type="checkbox" value="" id="flexCheckDefault" checked>
  <label class="form-check-label" for="flexCheckDefault">
    The URL for the cloud app hosted in Azure is <a href="https://azure-cloud-app.mcn-lab.f5demos.com">https://aws-cloud-app.mcn-lab.f5demos.com</a>  
  </label>
</div>
<div class="form-check">
  <input class="form-check-input" type="checkbox" value="" id="flexCheckDefault" checked>
  <label class="form-check-label" for="flexCheckCDefault">
    The cloud app is only reachable from the "student-azurenet" site.
  </label>
</div>
<div class="form-check">
  <input class="form-check-input" type="checkbox" value="" id="flexCheckDefault" checked>
  <label class="form-check-label" for="flexCheckCDefault">
    The cloud app is TLS enabled.
  </label>
</div>

<div style="height:25px"></div>


<div class="left-aligned-button-container">
    <button id="requestBtn2" class="btn btn-primary">Test Load Balancer</button>
</div>
<div id="result2" class="mt-3"></div>
<script>
document.getElementById('requestBtn2').addEventListener('click', () => {
    makeHttpRequest('requestBtn2', '/_lb2', 'result2');
});
</script>

<div style="height:25px"></div>

Once you've completed both exercises, move on to the <a href="/path" class="alert-link">path based routing</a> exercise.

<div style="height:25px"></div>

