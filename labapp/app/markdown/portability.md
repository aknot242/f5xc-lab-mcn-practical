<div href="/" class="d-flex align-items-center pb-3 mb-3 link-dark text-decoration-none">
    <img src="/static/manip.png" width="300px" height="auto" alt="intro">
</div>

# **Portability**

<div href="/" class="d-flex align-items-center pb-3 mb-3 link-dark text-decoration-none border-bottom"></div>


The configuration built so far handles load balancing, routing, and content manipulation.
XC refers to this object as a "load balancer" -- but it's really the holistic representation of an application whose service endpoints live across the distributed network.
The object is simple -- it doesn't yet include configuration for WAAP, API protection, or a service policy.

What seperate XC from traditional ADCs is the flexibility of defining <strong>where the object is advertised</strong>.

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
    makeHttpRequest('requestBtn1', '/_port1', 'result');
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

Do you have a friend working on the lab?
Ask them their ephemeral namespace and test that their load balancer is being advertised from your site.


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
    <button id="requestBtn2" class="btn btn-primary">Test Load Balancer</button>
</div>
<div id="result2" class="mt-3"></div>
<script>
document.getElementById('requestBtn2').addEventListener('click', () => {
    makeHttpRequest('requestBtn2', '/_manip2', 'result2');
});
</script>

<div  style="height:25px" class="d-flex align-items-center pb-3 mb-3 link-dark text-decoration-none border-bottom"></div>

🚀 Nice 🚀! 
</br>


