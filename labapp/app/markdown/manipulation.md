<div href="/" class="d-flex align-items-center pb-3 mb-3 link-dark text-decoration-none">
    <img src="/static/manip.png" width="300px" height="auto" alt="intro">
</div>

# **Manipulation**

<div href="/" class="d-flex align-items-center pb-3 mb-3 link-dark text-decoration-none border-bottom"></div>

Since web traffic has been traversing proxies, engineers have needed to alter HTTP content for increased observability ([XFF](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Forwarded-For)), performance ([cache-control](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Cache-Control)), or other reasons ([JWT](https://en.wikipedia.org/wiki/JSON_Web_Token)). 
"Proxy Pass" functionality has been part of web servers since the early Apache days.
Adding, removing, and altering Headers are tablestakes for ADCs, CDNs, and software-based load balancers.
F5 XC App Connect enables this functionality granularly on routes or broadly on the load balancer.


<div style="height:25px"></div>

### **Exercise 1: Path Rewrite**

Configure a path <strong>prefix rewrite</strong> to remove part of the request path when routing to an origin.

<ul class="list-group">
  <li class="list-group-item">
  <img src="/static/lb-icon.png" width="auto" height="50px"> &nbsp; &nbsp;
  Keep your configuration from the previous exercise in place. 
  </li>
  <li class="list-group-item">
  <img src="/static/route-icon.png" width="auto" height="50px"> &nbsp; &nbsp;
  Requests to <strong>https://<i>eph-ns</i>.mcn-lab.f5demos.com<u>/aws/raw</u></strong> need to arrive at the origin with a path of <strong>/raw</strong></u>.
  </li>
</ul>

<div style="height:25px"></div>

#### **Test Criteria**

```http
GET https://eph-ns.mcn-lab.f5demos.com/aws/raw HTTP/1.1
Host: eph-ns.mcn-lab.f5demos.com

{
  "info": {
    "path": "/raw"
  }
  ...
}
```

<div class="left-aligned-button-container">
    <button id="requestBtn1" class="btn btn-primary">Test Load Balancer</button>
</div>
<div id="result1" class="mt-3"></div>
<script>
document.getElementById('requestBtn1').addEventListener('click', () => {
    makeHttpRequest('requestBtn1', '/_manip1', 'result1');
});
</script>

Since questions on this functionality are often asked on <strong><a href="https://community.f5.com/" target="_blank">F5 DevCentral</a></strong>, a hint might be warranted. 

<div id="hints">
<p>
  <a class="btn btn-primary" data-bs-toggle="collapse" href="#multiCollapseExample1" role="button" aria-expanded="false" aria-controls="multiCollapseExample1">Route Hint</a>
  <button class="btn btn-primary" type="button" data-bs-toggle="collapse" data-bs-target="#multiCollapseExample2" aria-expanded="false" aria-controls="multiCollapseExample2">Rewrite Hint</button>
</p>
<div class="row">
      <div class="collapse multi-collapse" id="multiCollapseExample1" data-bs-parent="#hints">
      <img src="/static/rewrite1.png" width="900px" height="auto" alt="temp">
    </div>
  <div class="collapse multi-collapse" id="multiCollapseExample2" data-bs-parent="#hints">
    <div class="">
      <img src="/static/rewrite2.png" width="500px" height="auto" alt="temp">
    </div>
  </div>
</div>
</div>

<div style="height:25px"></div>

### **Exercise 2: Request Header Shenanigans**

While blind header insertion or deletion is useful in some use cases, this exercise focuses on context aware header manipulation. 
Use the <strong><a href="https://docs.cloud.f5.com/docs/how-to/advanced-security/configure-http-header-processing" target="_blank">XC Header Processing</a></strong> docs for reference. 

<div style="height:25px"></div>

<ul class="list-group">
  <li class="list-group-item">
  <img src="/static/lb-icon.png" width="auto" height="50px"> &nbsp; &nbsp;
  Insert a request header named <strong>X-MCN-src-site</strong> to identifies the UDF CE to the origin. <u>Do not use a static value</u>. 
  </li>
  <li class="list-group-item">
  <img src="/static/lb-icon.png" width="auto" height="50px"> &nbsp; &nbsp;
  Insert a request header named <strong>X-MCN-namespace</strong> to identifies the ephemeral namespace to the origin. <u>Do not use a static value</u>. 
  </li>
</ul>

<div style="height:25px"></div>

#### **Test Criteria**

```http
GET https://eph-ns.mcn-lab.f5demos.com/ HTTP/1.1
Host: eph-ns.mcn-lab.f5demos.com

{
  ...
  "request_headers": {
    "x-mcn-namespace": "wiggly-yellowtail",
    "x-mcn-src-site": "cluster-xxxxxxxx",
  },
  ...
}
```

<div class="left-aligned-button-container">
    <button id="requestBtn2" class="btn btn-primary">Test Load Balancer</button>
</div>
<div id="result2" class="mt-3"></div>
<script>
document.getElementById('requestBtn2').addEventListener('click', () => {
    makeHttpRequest('requestBtn2', '/_manip2', 'result2');
});
</script>

<div style="height:25px"></div>

### **Exercise 3: Response Header Shenanigans**

<div style="height:25px"></div>

<ul class="list-group">
  <li class="list-group-item">
  <img src="/static/lb-icon.png" width="auto" height="50px"> &nbsp; &nbsp;
  Insert a response header named <strong>X-MCN-dst-site</strong> to determine which cloud CE processed the request. 
  </li>
</ul>

<div style="height:25px"></div>

#### **Test Criteria**

<div style="height:25px"></div>

<strong><u>This test will evaluate response headers.</u></strong>

```http
GET https://eph-ns.mcn-lab.f5demos.com/aws HTTP/1.1
Host: eph-ns.mcn-lab.f5demos.com

{
  "x-mcn-dest-site": "student-awsnet"
}
```

```http
GET https://eph-ns.mcn-lab.f5demos.com/azure HTTP/1.1
Host: eph-ns.mcn-lab.f5demos.com

{
  "x-mcn-dest-site": "student-azurenet"
}
```

<div class="left-aligned-button-container">
    <button id="requestBtn3" class="btn btn-primary">Test Load Balancer</button>
</div>
<div id="result3" class="mt-3"></div>
<script>
document.getElementById('requestBtn3').addEventListener('click', () => {
    makeHttpRequest('requestBtn3', '/_manip3', 'result3');
});
</script>


<div  style="height:25px" class="d-flex align-items-center pb-3 mb-3 link-dark text-decoration-none border-bottom"></div>

<nav aria-label="labapp nav">
    <ul class="pagination justify-content-end">
      <li class="page-item">
        <a class="page-link" href="/portability">Portability <i class="bi bi-arrow-right-circle-fill"></i></a>
      </li>
    </ul>
  </nav>

