<div href="/" class="d-flex align-items-center pb-3 mb-3 link-dark text-decoration-none">
    <img src="/static/path.png" width="300px" height="auto" alt="intro">
</div>

# **HTTP Routing**

<div href="/" class="d-flex align-items-center pb-3 mb-3 link-dark text-decoration-none border-bottom"></div>

Modern applications, and some classic ones, are often comprised of disparate services spread across sites. 
MCN solutions must be able to make routing decisions based on characterstics of an HTTP request.
F5 XC App Connect is a distributed L7 proxy that provide intelligent routing, visibility, and strategic points of control.

<div style="height:25px"></div>

### **Exercise 1: Path Routing**

Build routing rules and configure your load balancer to route traffic between the two cloud apps based on the request url.

<ul class="list-group">
  <li class="list-group-item">
  <img src="/static/origin-icon.png" width="auto" height="50px"> &nbsp; &nbsp;
  Reuse the origin pools from the previous exercise
  </li>
  <li class="list-group-item">
  <img src="/static/route-icon.png" width="auto" height="50px"> &nbsp; &nbsp;
  Route requests to "<u>https://<i>eph-ns</i>.mcn-lab.f5demos.com/<strong>aws</strong></u>" to the AWS cloud app. 
  </li>
  <li class="list-group-item">
  <img src="/static/route-icon.png" width="auto" height="50px"> &nbsp; &nbsp;
  Route requests to "<u>https://<i>eph-ns</i>.mcn-lab.f5demos.com/<strong>azure</strong></u>" to the Azure cloud app. 
  </li>
</ul>

<div style="height:25px"></div>

#### **Test Criteria**

```http
GET https://eph-ns.mcn-lab.f5demos.com/aws/raw HTTP/1.1
Host: eph-ns.mcn-lab.f5demos.com

{
  "env": "aws",
  ...
}
```

```http
GET https://eph-ns.mcn-lab.f5demos.com/azure/raw HTTP/1.1
Host: eph-ns.mcn-lab.f5demos.com

{
  "env": "azure",
  ...
}
```

<div style="height:25px"></div>

<div class="left-aligned-button-container">
    <button id="requestBtn1" class="btn btn-primary">Test Load Balancer</button>
</div>
<div id="result1" class="mt-3"></div>
<script>
document.getElementById('requestBtn1').addEventListener('click', () => {
    makeHttpRequest('requestBtn1', '/_route1', 'result1');
});
</script>

<div  style="height:25px" class="d-flex align-items-center pb-3 mb-3 link-dark text-decoration-none border-bottom"></div>

### **Exercise 2: Header Routing**

Build rules to route traffic between the two cloud apps based on an arbitrary HTTP request header.


<ul class="list-group">
  <li class="list-group-item">
  <img src="/static/route-icon.png" width="auto" height="50px"> &nbsp; &nbsp;
  Route requests with an "<strong>X-MCN-Lab: aws</strong>" header to the AWS cloud app.
  </li>
  <li class="list-group-item">
  <img src="/static/route-icon.png" width="auto" height="50px"> &nbsp; &nbsp;
  Route requests with an "<strong>X-MCN-Lab: azure</strong>" header to the Azure cloud app.
  </li>
</ul>

<div style="height:25px"></div>

#### **Test Criteria**

```http
GET https://eph-ns.mcn-lab.f5demos.com/raw HTTP/1.1
Host: eph-ns.mcn-lab.f5demos.com
X-MCN-lab: aws

{
  "env": "aws",
  ...
}
```

```http
GET https://eph-ns.mcn-lab.f5demos.com/raw HTTP/1.1
Host: eph-ns.mcn-lab.f5demos.com
X-MCN-lab: azure

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
    makeHttpRequest('requestBtn2', '/_route2', 'result2');
});
</script>

<div  style="height:25px" class="d-flex align-items-center pb-3 mb-3 link-dark text-decoration-none border-bottom"></div>

<nav aria-label="labapp nav">
    <ul class="pagination justify-content-end">
      <li class="page-item">
        <a class="page-link" href="/manipulation">Manipulation <i class="bi bi-arrow-right-circle-fill"></i></a>
      </li>
    </ul>
  </nav>