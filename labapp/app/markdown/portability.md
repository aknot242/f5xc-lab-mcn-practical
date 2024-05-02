<div href="/" class="d-flex align-items-center pb-3 mb-3 link-dark text-decoration-none">
    <img src="/static/portable.png" width="300px" height="auto" alt="intro">
</div>

# **Portability**

<div href="/" class="d-flex align-items-center pb-3 mb-3 link-dark text-decoration-none border-bottom"></div>


The configuration built so far handles load balancing, routing, and content manipulation.
XC refers to this object as a "load balancer" -- but it's really the holistic representation of an application whose service endpoints live across the distributed network.
The object is simple -- it doesn't yet include configuration for WAAP, API protection, or a service policy.

What seperates XC from traditional ADCs is flexibility in defining <strong>where a load balancer is advertised</strong>.

<div style="height:25px"></div>

### **Exercise 1: Advertise Policy**

<ul class="list-group">
  <li class="list-group-item">
  <img src="/static/lb-icon.png" width="auto" height="50px"> &nbsp; &nbsp;
  Configure the load balancer to be advertised on the virtual site <strong>shared/mcn-practical-udf-sites</strong>. 
  </li>
</ul>

<div style="height:25px"></div>

#### **Test Criteria**

```http
GET https://eph-ns.mcn-lab.f5demos.com/ HTTP/1.1
Host: eph-ns.mcn-lab.f5demos.com

{
  "info": {
    "path": "/"
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
    makeHttpRequest('requestBtn1', '/_port1', 'result1');
});
</script>


<div id="hints">
<p>
  <a class="btn btn-primary" data-bs-toggle="collapse" href="#multiCollapseExample1" role="button" aria-expanded="false" aria-controls="multiCollapseExample1">Why did that work?</a>
</p>
<div class="row">
      <div class="collapse multi-collapse" id="multiCollapseExample1" data-bs-parent="#hints">
      <img src="/static/vsite2.png" width="600px" height="auto" alt="temp">
      <img src="/static/vsite.png" width="900px" height="auto" alt="temp">
    </div>
</div>
</div>

<div style="height:25px"></div>

### **Exercise 2: Find a Friend**

Do you have a friend working on the lab? Find thier <strong>ephemeral namespace</strong> (or use the one provided).

<ul class="list-group">
  <li class="list-group-item">
  <img src="/static/lb-icon.png" width="auto" height="50px"> &nbsp; &nbsp;
  Test if your friend's load balancer is being advertised to the UDF site.
  </li>
</ul>

<div style="height:25px"></div>

#### **Test Criteria**

```http
GET https://eph-ns.mcn-lab.f5demos.com/ HTTP/1.1
Host: eph-ns.mcn-lab.f5demos.com

{
  "info": {
    "path": "/"
  }
  ...
}
```

<div class="container mt-4">
    <div class="row">
        <div class="col-md-6">
            <div class="input-group mb-3">
                <input type="text" id="inputText2" class="form-control"
                  placeholder="Enter your string here" aria-label="User input" value="wiggly-yellowtail">
                <button id="requestBtn2" class="btn btn-primary" type="button">Test Load Balancer</button>
            </div>
        </div>
    </div>
    <div id="result2" class="mt-3"></div>
</div>
<script>
document.getElementById('requestBtn2').addEventListener('click', () => {
    makePostRequest('requestBtn2', '/_port2', 'result2', 'inputText2');
});
</script>

<div  style="height:25px" class="d-flex align-items-center pb-3 mb-3 link-dark text-decoration-none border-bottom"></div>

<nav aria-label="labapp nav">
    <ul class="pagination justify-content-end">
      <li class="page-item">
        <a class="page-link" href="/score">Scoreboard <i class="bi bi-arrow-right-circle-fill"></i></a>
      </li>
    </ul>
  </nav>